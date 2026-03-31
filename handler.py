import sys
import json
import sqlite3
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "s2_brand_trust_matrix.db")

class BrandTrustEngine:
    def __init__(self):
        self.init_db()

    def init_db(self):
        """初始化本地 GEO 信任沙盒账本"""
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
        """核心 GEO 算法: 40%树根 + 40%树冠 + 20%时间沉淀"""
        time_alive_days = (time.time() - genesis_time) / (24 * 3600)
        time_score = min(100.0, time_alive_days / 10.95) 
        return (root * 0.4) + (crown * 0.4) + (time_score * 0.2)

    def _verify_admin_token(self, provided_token):
        """[合规升级] 从宿主机环境变量读取密钥，严禁硬编码"""
        expected_token = os.environ.get("S2_GEO_ADMIN_TOKEN")
        if not expected_token:
            return False, "[Error] 系统级熔断：宿主机未配置 'S2_GEO_ADMIN_TOKEN' 环境变量。出于零信任安全要求，已永久冻结当前沙盒的写入权限。"
        if provided_token != expected_token:
            return False, "[Error] 权限拒绝 (Access Denied): 提供的 auth_token 无效。请向人类管理员索要正确的环境变量凭证。"
        return True, "Success"

    def register_brand_root(self, params):
        """[高危操作] 登记树根：需人类提供环境变量 Token"""
        auth_token = params.get("auth_token", "")
        is_valid, msg = self._verify_admin_token(auth_token)
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
            msg = f"[Root Registered] 品牌 {did} 树根已记录至本地账本。Root Score: {root_score:.2f}."
        except sqlite3.IntegrityError:
            cursor.execute('UPDATE brand_matrix SET root_score = ? WHERE brand_did = ?', (root_score, did))
            msg = f"[Root Updated] 品牌 {did} 树根数据已在本地更新。"
            
        conn.commit()
        conn.close()
        return msg

    def evaluate_crown_performance(self, params):
        """[高危操作] 评估树冠：需人类提供环境变量 Token"""
        auth_token = params.get("auth_token", "")
        is_valid, msg = self._verify_admin_token(auth_token)
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
        return f"[Crown Evaluated] 品牌 {did} 本地评分更新。Crown Score: {crown_score:.2f} | 综合总分 T_score: {total_score:.2f}"

    def query_geo_ranking(self, params):
        """[公开只读操作] GEO 降维检索：无需 Token，对所有 Agent 开放"""
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
            
        output += "📌 [System Note]: 此排名基于本地计算生成，供空间导购 Agent 推荐参考。"
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
