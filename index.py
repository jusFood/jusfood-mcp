from mcp.server.fastmcp import FastMCP
import requests
from typing import List
from tabulate import tabulate
import json

mcp = FastMCP("jusfood")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# get all coffee shop
@mcp.tool()
def get_shop_info() -> str:
    """Get coffee shop info based
    
    Returns:
        Formatted table string containing cafe information
    """
    # 發送 GET 請求獲取所有商店資訊
    response = requests.get('https://backtestdog.ddns.net/jusfood/cafe/api/cafe-locations')
    data = response.json()
    
    # 準備表格數據
    table_data = []
    for cafe in data['locations']:
        table_data.append([
            cafe['name'],
            cafe['address'],
            f"({cafe['coordinates']['latitude']}, {cafe['coordinates']['longitude']})"
        ])
    
    # 創建表格
    headers = ['店名', '地址', '經緯度']
    table = tabulate(table_data, headers=headers, tablefmt='grid')
    
    return table

# get coffee shop by features
@mcp.tool()
def get_shop_by_features(features: str) -> str:
    """Get coffee shops filtered by specific features
    
    Args:
        features: Space-separated feature strings (e.g. "安静")
    
    Returns:
        Formatted table string containing filtered cafe information
    """
    try:
        # 將輸入的字串分割成列表
        feature_list = features.split()
        
        # 準備請求體
        request_data = {
            "features": feature_list,
            "include_conditional": True
        }
        
        # 發送 POST 請求
        response = requests.post(
            'https://backtestdog.ddns.net/jusfood/cafe/api/search/features',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json=request_data
        )
        
        # 檢查回應狀態
        if response.status_code != 200:
            return f"API 請求失敗，狀態碼: {response.status_code}"
            
        # 解析回應數據
        data = response.json()
        
        # 如果沒有結果
        if not data.get('results'):
            return f"沒有找到符合「{features}」的咖啡廳"
            
        # 準備表格數據
        table_data = []
        for cafe in data['results']:
            # 處理評分資訊（如果有的話）
            ratings = cafe.get('top_ratings', [])
            ratings_str = ' | '.join([f"{r[0]}: {r[1]}" for r in ratings[:2]]) if ratings else 'N/A'
            
            # 處理特徵資訊
            matched_features = cafe.get('matched_features', [])
            features_str = ', '.join(matched_features) if matched_features else 'N/A'
            
            # 添加咖啡廳資訊到表格
            table_data.append([
                cafe['name'],
                f"{cafe['city']}{cafe['district']}",
                cafe['address'],
                f"{cafe.get('feature_matches', 0)}/{len(feature_list)}",
                f"{cafe.get('relevance', 0):.2f}",
                features_str,
                ratings_str
            ])
            
        # 創建表格
        headers = ['店名', '地區', '地址', '特徵匹配數', '相關性', '匹配特徵', '評分']
        table = tabulate(
            table_data,
            headers=headers,
            tablefmt='grid',
            maxcolwidths=[20, 10, 30, 10, 10, 30, 20]
        )
        
        # 顯示搜尋資訊
        search_info = (
            f"\n搜尋條件: {', '.join(feature_list)}\n"
            f"總共找到: {data.get('total_count', len(table_data))} 間咖啡廳"
        )
        
        return table + search_info
        
    except requests.exceptions.RequestException as e:
        return f"網路請求錯誤: {str(e)}"
    except json.JSONDecodeError as e:
        return f"JSON 解析錯誤: {str(e)}"
    except Exception as e:
        return f"發生未預期的錯誤: {str(e)}"