#!/usr/bin/env python3
"""使用 akshare + 绕过代理 批量获取半导体板块数据"""
import os
os.environ['NO_PROXY'] = 'eastmoney.com,push2.eastmoney.com,push2his.eastmoney.com,79.push2.eastmoney.com,datainterface.eastmoney.com,gtimg.cn,qq.com'
os.environ['no_proxy'] = os.environ['NO_PROXY']

import akshare as ak
import pandas as pd
import json
from datetime import datetime, timedelta

OUTPUT_DIR = r"D:\Contents\research\2026-07-30_半导体板块涨跌复盘"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 绕过代理的session
import requests
session = requests.Session()
session.trust_env = False  # 不使用系统代理设置

# 用猴子补丁绕过代理
import urllib.request
_proxy_handler = urllib.request.ProxyHandler({})
_opener = urllib.request.build_opener(_proxy_handler)
urllib.request.install_opener(_opener)

results = {}
semi_codes = ['603501','300661','603986','002049','300782','603160','688256','688008',
             '688521','688536','688981','688347','688396','600584','002185','002156',
             '603005','002371','688012','688072','300604','688126','688019','300655',
             '603650','688200','688206','603290','300623','688187']

def safe_fetch(name, fn, *args, **kwargs):
    try:
        data = fn(*args, **kwargs)
        if isinstance(data, pd.DataFrame) and len(data) > 0:
            print(f"  [{name}] OK: {len(data)} rows")
            results[name] = data.to_dict('records')
            return data
        else:
            print(f"  [{name}] EMPTY or wrong type: {type(data).__name__}")
            return data
    except Exception as e:
        print(f"  [{name}] FAIL: {e}")
        return None

# ============================================================
# 1. 行业板块行情 (ths数据源) - 已验证可用
# ============================================================
print("="*60)
print("1. 行业板块行情 (同花顺)")
df = safe_fetch("board_industry", ak.stock_board_industry_index_ths)
if df is not None:
    # df可能是返回的原始数据 - 检查实际列名
    print(f"  columns: {list(df.columns)[:10]}")
    cols = list(df.columns)
    # 查找半导体
    for name_col in ['板块名称', 'name', '板块', '行业名称']:
        if name_col in cols:
            semi = df[df[name_col].str.contains('半导|芯片', na=False)]
            print(f"  半导体相关: {len(semi)}条")
            for _, r in semi.iterrows():
                vals = {c: r.get(c, 'N/A') for c in cols[:8]}
                print(f"    {vals}")
            break

# ============================================================
# 2. 概念板块行情 (ths)
# ============================================================
print("\n2. 概念板块行情 (同花顺)")
try:
    df2 = ak.stock_board_concept_index_ths()
    print(f"  columns: {list(df2.columns)[:10]}")
    keywords = ['HBM','先进封装','光刻机','光刻胶','第三代半导体','IGBT','碳化硅',
                '氮化镓','汽车芯片','存储芯片','Chiplet','EDA','RISC-V','AI芯片']
    cols = list(df2.columns)
    name_col = next((c for c in cols if '名称' in c or 'name' in c.lower()), cols[0])
    for kw in keywords:
        m = df2[df2[name_col].str.contains(kw, na=False)]
        if len(m) > 0:
            for _, r in m.iterrows():
                print(f"  {r[name_col]}: {r.iloc[1] if len(r)>1 else 'N/A'}")
    results['board_concept'] = df2.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 3. 概念板块成分股 (em数据源，测试绕过代理)
# ============================================================
print("\n3. 半导体概念成分股")
try:
    df3 = ak.stock_board_concept_cons_em(symbol="半导体概念")
    print(f"  成分股: {len(df3)}只")
    print(f"  columns: {list(df3.columns)[:10]}")
    results['concept_members'] = df3.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 4. 概念板块历史K线 (em数据源)
# ============================================================
print("\n4. 半导体概念日K线")
try:
    df4 = ak.stock_board_concept_hist_em(symbol="半导体概念", period="日k",
                                          start_date="20260501", end_date="20260730")
    july_k = df4[df4['日期'].astype(str).str.contains('2026-07')]
    print(f"  7月K线: {len(july_k)}天")
    if len(july_k) > 0:
        o0 = july_k.iloc[0]['开盘']
        cn = july_k.iloc[-1]['收盘']
        hi = july_k['最高'].max()
        lo = july_k['最低'].min()
        print(f"  7月: 开{o0:.0f} 收{cn:.0f} 高{hi:.0f} 低{lo:.0f} 涨{(cn/o0-1)*100:+.1f}%")
        for _, r in july_k.iterrows():
            chg = (r['收盘']/r['开盘']-1)*100
            amp = (r['最高']/r['最低']-1)*100
            vol = r.get('成交量',0)/1e8
            amt = r.get('成交额',0)/1e8
            print(f"    {r['日期']}: O{r['开盘']:.0f} C{r['收盘']:.0f} ({chg:+.1f}%) 振{amp:.1f}% 额{amt:.0f}亿")
        results['semi_kline'] = july_k.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 5. 行业资金流排名
# ============================================================
print("\n5. 行业板块资金流向")
try:
    df5 = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
    print(f"  columns: {list(df5.columns)[:10]}")
    # 查找半导体
    cols5 = list(df5.columns)
    name_c = next((c for c in cols5 if '名称' in c or 'name' in c.lower()), cols5[1] if len(cols5)>1 else cols5[0])
    semi_flow = df5[df5[name_c].str.contains('半导|芯片', na=False)]
    for _, r in semi_flow.iterrows():
        print(f"  {dict(r)}")
    results['sector_fund_flow'] = df5.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 6. 北向资金历史
# ============================================================
print("\n6. 北向资金历史")
try:
    df6 = ak.stock_hsgt_hist_em(symbol="沪股通")
    print(f"  columns: {list(df6.columns)[:10]}")
    july = df6[df6['日期'].astype(str).str.contains('2026-07')]
    print(f"  沪股通7月: {len(july)}天")
    for _, r in july.iterrows():
        print(f"    {r['日期']}: {dict(r)}")
    results['north_flow_sh'] = july.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

try:
    df6b = ak.stock_hsgt_hist_em(symbol="深股通")
    july_sz = df6b[df6b['日期'].astype(str).str.contains('2026-07')]
    print(f"  深股通7月: {len(july_sz)}天")
    for _, r in july_sz.iterrows():
        print(f"    {r['日期']}: {dict(r)}")
    results['north_flow_sz'] = july_sz.to_dict('records')
except Exception as e:
    print(f"  深股通 FAIL: {e}")

# ============================================================
# 7. 北向资金个股持仓
# ============================================================
print("\n7. 北向资金持股")
try:
    df7 = ak.stock_hsgt_hold_stock_em(market="沪股通")
    print(f"  columns: {list(df7.columns)[:10]}")
    semi_hold = df7[df7['名称'].apply(
        lambda x: any(k in str(x) for k in 
            ['中芯','韦尔','豪威','兆易','北方','中微','紫光','寒武','澜起',
             '长电','华天','通富','卓胜','圣邦','斯达','拓荆','长川']))]
    print(f"  半导体北向持股: {len(semi_hold)}只")
    for _, r in semi_hold.iterrows():
        print(f"    {r['名称']}({r['代码']}): {dict(r)}")
    results['north_holding_sh'] = semi_hold.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 8. 龙虎榜 (最近)
# ============================================================
print("\n8. 龙虎榜详情")
try:
    # 先看函数签名
    import inspect
    sig = inspect.signature(ak.stock_lhb_detail_em)
    print(f"  stock_lhb_detail_em params: {list(sig.parameters.keys())}")
    
    # 尝试不同调用方式
    try:
        df8 = ak.stock_lhb_detail_em(start_date="20260701", end_date="20260730")
    except:
        try:
            df8 = ak.stock_lhb_detail_em(date="20260701")
        except:
            df8 = ak.stock_lhb_detail_em()
    
    if isinstance(df8, pd.DataFrame):
        print(f"  columns: {list(df8.columns)[:10]}")
        print(f"  total: {len(df8)} records")
        results['lhb_raw'] = df8.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 9. ETF行情
# ============================================================
print("\n9. ETF实时行情")
try:
    df9 = ak.fund_etf_spot_em()
    etf_codes_list = ['159995','512480','159813','516640','588000','588200']
    etf_spot = df9[df9['代码'].isin(etf_codes_list)]
    for _, r in etf_spot.iterrows():
        print(f"  {r['名称']}({r['代码']}): 净值{r['最新价']} 涨跌{r.get('涨跌幅',0):.2f}% "
              f"成交额{r.get('成交额',0)/1e8:.2f}亿")
    results['etf_spot'] = etf_spot.to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 10. 个股资金流
# ============================================================
print("\n10. 个股资金流向")
try:
    sig = inspect.signature(ak.stock_individual_fund_flow)
    print(f"  stock_individual_fund_flow params: {list(sig.parameters.keys())}")
    
    df10 = ak.stock_individual_fund_flow(stock="603501", market="sh")
    if isinstance(df10, pd.DataFrame):
        print(f"  columns: {list(df10.columns)[:10]}")
        print(f"  rows: {len(df10)}")
        results['fund_flow_sample'] = df10.tail(5).to_dict('records')
except Exception as e:
    print(f"  FAIL: {e}")

# ============================================================
# 保存
# ============================================================
print("\n" + "="*60)
print("保存数据...")

with open(os.path.join(OUTPUT_DIR, "akshare_data.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2, default=str)

print(f"数据已保存: {OUTPUT_DIR}/akshare_data.json")
print(f"共 {len(results)} 个数据集")
print("Done!")
