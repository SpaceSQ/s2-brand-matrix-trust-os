import sys
import json
import sqlite3
import time
import os
import hmac
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "s2_brand_trust_matrix.db")

class BrandTrustEngine:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS brand_matrix (
                brand_did TEXT PRIMARY KEY,
                suns_address TEXT,
                industry_category TEXT,
                root_score REAL DEFAULT 0.0,
                crown_score REAL DEFAULT 0.0,
                genesis_timestamp REAL,
                total_trust_score REAL DEFAULT 0.0
            )
        ''')
        conn.commit()
        conn.close()

    def calculate_total_score(self, root, crown, genesis_time):
        time_alive_days = (time.time() - genesis_time) / (24 * 3600)
        time_score = min(100.0, time_alive_days / 10.95) 
        return (root * 0.4) + (crown * 0.4) + (time_score * 0.2)

    def _verify_hmac_signature(self, params):
        """[密码学合规] 验证 HMAC-SHA256 签名，确保请求不可篡改且来源合法"""
        secret = os.environ.get("S2_GEO_ADMIN_TOKEN")
        if not secret or len(secret) < 16:
            return False, "[Error] 系统级熔断: 宿主机 'S2_GEO_ADMIN_TOKEN' 缺失或密码强度不足(需>=16字符)。"

        signature = params.get("signature", "")
        if not signature:
            return False, "[Error] 权限拒绝: 缺失 HMAC-SHA256 签名 (signature 字段)。禁止写入。"

        # 构建验签 payload (排除 signature 字段本身)
        payload = {k: v for k, v in params.items() if k != "signature"}
        payload_str = json.dumps(payload, sort_keys=True)
        
        # 计算期望的签名
        expected_sig = hmac.new(secret.encode('utf-8'), payload_str.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # 安全的常量时间比较 (防时序攻击)
        if not hmac.compare_digest(expected_sig, signature):
            return False, "[Error] 签名校验失败 (Invalid Signature): 数据篡改或密钥不匹配。"
            
        return True, "Success"

    def register_brand_root(self, params):
        """[高危操作] 登记树根：执行严格的 HMAC-SHA256 签名校验"""
        is_valid, msg = self._verify_hmac_signature(params)
        if not is_valid:
            return msg

        did = params.get("brand_did", "")
        suns = params.get("suns_address", "")
        category = params.get("industry_category", "General")
        patents = int(params.get("patents_count", 0))
        esg = params.get("esg_rating", "C").upper()

        esg_multiplier = {"A": 1.0, "B": 0.8, "C": 0.5}.get(esg, 0.3)
        root_score = min(100.0, (patents * 0.5)) * esg_multiplier

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        current_time = time.time()
        
        try:
            cursor.execute('''
                INSERT INTO brand_matrix (brand_did, suns_address, industry_category, root_score, genesis_timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (did, suns, category, root_score, current_time))
            msg = f"[Root Registered] 品牌 {did} 树根已记录。Root Score: {root_score:.2f}."
        except sqlite3.IntegrityError:
            cursor.execute('UPDATE brand_matrix SET root_score = ? WHERE brand_did = ?', (root_score, did))
            msg = f"[Root Updated] 品牌 {did} 树根数据已更新。"
            
        conn.commit()
        conn.close()
        return msg

    def evaluate_crown_performance(self, params):
        """[高危操作] 评估树冠：执行严格的 HMAC-SHA256 签名校验"""
        is_valid, msg = self._verify_hmac_signature(params)
        if not is_valid:
            return msg

        did = params.get("brand_did", "")
        contracts = int(params.get("smart_contracts_completed", 0))
        violations = int(params.get("service_violations", 0))

        crown_score = max(0.0, min(100.0, (contracts * 2.0) - (violations * 20.0)))

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT root_score, genesis_timestamp FROM brand_matrix WHERE brand_did = ?', (did,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return f"[Error] 品牌 {did} 尚未注册，无法更新树冠。"
            
        root_score, genesis_timestamp = row
        total_score = self.calculate_total_score(root_score, crown_score, genesis_timestamp)

        cursor.execute('''
            UPDATE brand_matrix 
            SET crown_score = ?, total_trust_score = ? 
            WHERE brand_did = ?
        ''', (crown_score, total_score, did))
        
        conn.commit()
        conn.close()
        return f"[Crown Evaluated] 品牌 {did} 本地评分更新。Crown Score: {crown_score:.2f} | T_score: {total_score:.2f}"

    def query_geo_ranking(self, params):
        """[公开操作] GEO 降维检索 (无需鉴权)"""
        category = params.get("industry_category", "")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT suns_address, brand_did, total_trust_score 
            FROM brand_matrix 
            WHERE industry_category = ? 
            ORDER BY total_trust_score DESC 
            LIMIT 3
        ''', (category,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return f"[GEO 检索为空] 在 {category} 领域暂无登记的主权品牌。"
            
        output = f"=== S2 GEO Local Ranking for [{category}] ===\n"
        for i, (suns, did, score) in enumerate(results, 1):
            output += f"Rank {i}: {suns} (DID: {did}) | Trust Score: {score:.2f}\n"
            
        return output

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        request = json.loads(input_data)
        action = request.get("action")
        params = request.get("params", {})
        
        engine = BrandTrustEngine()
        if action == "register_brand_root": result = engine.register_brand_root(params)
        elif action == "evaluate_crown_performance": result = engine.evaluate_crown_performance(params)
        elif action == "query_geo_ranking": result = engine.query_geo_ranking(params)
        else: result = "Unknown Trust OS Action."
        
        print(json.dumps({"status": "success", "output": result}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
