#!/usr/bin/env python3
"""使用 akshare 批量获取半导体板块数据"""
import akshare as ak
import pandas as pd
import json
import os
import sys
from datetime import datetime

OUTPUT_DIR = r"D:\Contents\research\2026-07-30_半导体板块涨跌复盘"
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = {}
semi_codes = ['603501','300661','603986','002049','300782','603160','688256','688008',
             '688521','688536','688981','688347','688396','600584','002185','002156',
             '603005','002371','688012','688072','300604','688126','688019','300655',
             '603650','688200','688206','603290','300623','688187']

def log(msg):
    print(msg, flush=True)

# ============================================================
# 1. 行业板块 + 概念板块行情
# ============================================================
log("="*60)
log("1. 行业板块行情")

try:
    df = ak.stock_board_industry_index_ths()
    log(f"  行业板块: {len(df)}条")
    semi = df[df['板块名称'].str.contains('半导|芯片', na=False)]
    for _, r in semi.iterrows():
        log(f"    {r['板块名称']}: {r.get('涨跌幅',0):.2f}% PE={r.get('市盈率',0):.2f} 总市值={r.get('总市值',0)/1e8:.0f}亿")
    results['board_industry'] = df.to_dict('records')
except Exception as e:
    log(f"  FAIL: {e}")

log("\n2. 概念板块行情")
try:
    df2 = ak.stock_board_concept_name_em()
    keywords = ['HBM','先进封装','光刻机','光刻胶','第三代半导体','IGBT','碳化硅',
                '氮化镓','汽车芯片','存储芯片','Chiplet','EDA','RISC-V','AI芯片',
                '半导体概念','汽车芯片','MCU芯片','模拟芯片']
    for kw in keywords:
        m = df2[df2['板块名称'].str.contains(kw, na=False)]
        if len(m) > 0:
            for _, r in m.iterrows():
                log(f"  {r['板块名称']}: {r.get('涨跌幅',0):.2f}%")
    results['board_concept'] = df2.to_dict('records')
except Exception as e:
    log(f"  FAIL: {e}")

# ============================================================
# 3. 北向资金
# ============================================================
log("\n" + "="*60)
log("3. 北向资金数据")
try:
    df_sh = ak.stock_hsgt_north_net_flow_in_em(symbol="沪股通")
    df_sz = ak.stock_hsgt_north_net_flow_in_em(symbol="深股通")
    july_sh = df_sh[df_sh['日期'].astype(str).str.contains('2026-07')]
    july_sz = df_sz[df_sz['日期'].astype(str).str.contains('2026-07')]
    log(f"  沪股通7月: {len(july_sh)}天  深股通7月: {len(july_sz)}天")
    for _, r in july_sh.iterrows():
        log(f"    沪 {r['日期']}: {r['当日净流入']:.2f}亿")
    for _, r in july_sz.iterrows():
        log(f"    深 {r['日期']}: {r['当日净流入']:.2f}亿")
    results['north_flow_sh'] = july_sh.to_dict('records')
    results['north_flow_sz'] = july_sz.to_dict('records')
except Exception as e:
    log(f"  FAIL: {e}")

# ============================================================
# 4. 半导体概念指数历史K线
# ============================================================
log("\n" + "="*60)
log("4. 半导体概念指数日K线")
try:
    df_k = ak.stock_board_concept_hist_em(symbol="半导体概念", period="日k", 
                                           start_date="20260501", end_date="20260730")
    july_k = df_k[df_k['日期'].astype(str).str.contains('2026-07')]
    log(f"  7月K线: {len(july_k)}天")
    o0 = july_k.iloc[0]['开盘']
    cn = july_k.iloc[-1]['收盘']
    hi = july_k['最高'].max()
    lo = july_k['最低'].min()
    log(f"  7月: 开{o0:.0f} 收{cn:.0f} 高{hi:.0f} 低{lo:.0f} 涨{(cn/o0-1)*100:+.1f}%")
    for _, r in july_k.iterrows():
        chg = (r['收盘']/r['开盘']-1)*100
        amp = (r['最高']/r['最低']-1)*100
        vol_unit = r.get('成交量',0)/1e8
        log(f"    {r['日期']}: O{r['开盘']:.0f} C{r['收盘']:.0f} ({chg:+.1f}%) 振幅{amp:.1f}% 成交{vol_unit:.1f}亿手")
    results['semi_concept_kline'] = july_k.to_dict('records')
except Exception as e:
    log(f"  FAIL: {e}")

# ============================================================
# 5. 行业资金流向
# ============================================================
log("\n" + "="*60)
log("5. 行业板块资金流向")
try:
    df_fund = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流向")
    semi_flow = df_fund[df_fund['名称'].str.contains('半导|芯片', na=False)]
    for _, r in semi_flow.iterrows():
        net = r.get('主力净流入-净额', 0)/1e8
        ratio = r.get('主力净流入-净占比', 0)
        log(f"  {r['名称']}: 主力{net:+.2f}亿 ({ratio:+.2f}%) 涨跌{r.get('涨跌幅',0):.2f}%")
    results['sector_fund_flow'] = semi_flow.to_dict('records')
except Exception as e:
    log(f"  FAIL: {e}")

# ============================================================
# 6. 龙虎榜 (7月)
# ============================================================
log("\n" + "="*60)
log("6. 龙虎榜数据 (7月半导体)")
all_lhb = []
for day in range(1, 31):
    try:
        dt = datetime(2026, 7, day)
        if dt.weekday() >= 5: continue
        if dt > datetime.now(): break
        ds = f"202607{day:02d}"
        try:
            lhb = ak.stock_lhb_detail_em(date=ds)
            for _, r in lhb.iterrows():
                code = str(r.get('代码', ''))
                if code in semi_codes:
                    all_lhb.append({
                        "日期": str(r.get('日期', '')),
                        "代码": code,
                        "名称": str(r.get('名称', '')),
                        "涨跌幅": float(r.get('涨跌幅', 0)),
                        "净买额": float(r.get('净买额', 0)),
                        "买入额": float(r.get('买入额', 0)),
                        "卖出额": float(r.get('卖出额', 0)),
                        "上榜原因": str(r.get('上榜原因', '')),
                    })
        except Exception as e2:
            log(f"  龙虎榜 {ds}: {e2}")
            pass
    except: break

log(f"  半导体龙虎榜: {len(all_lhb)}条")
for r in all_lhb[:30]:
    log(f"    {r['日期']} {r['名称']}({r['代码']}): 涨{r['涨跌幅']:.1f}% 净买{r['净买额']/1e4:.1f}万 [{r['上榜原因']}]")
results['lhb'] = all_lhb

# ============================================================
# 7. ETF历史数据
# ============================================================
log("\n" + "="*60)
log("7. ETF数据")
etf_codes = ["159995", "512480", "159813", "516640", "588000", "588200"]
etf_names = ["芯片ETF华夏", "半导体ETF国联安", "半导体ETF鹏华", "芯片龙头ETF", "科创50ETF", "科创芯片ETF"]
for code, name in zip(etf_codes, etf_names):
    try:
        df = ak.fund_etf_hist_em(symbol=code, period="daily", start_date="20260701", 
                                  end_date="20260730", adjust="")
        if len(df) > 0:
            log(f"  {name}({code}): {len(df)}天")
            for _, r in df.iterrows():
                vol_e = r.get('成交额', 0)/1e8
                log(f"    {r['日期']}: 收{r.get('收盘',0):.3f} 额{vol_e:.2f}亿")
            results[f"etf_{code}"] = df.to_dict('records')
    except Exception as e:
        log(f"  {name}({code}): {e}")

# ============================================================
# 8. 个股资金流 (主力净流入等)
# ============================================================
log("\n" + "="*60)
log("8. 个股资金流向")
# 获取半导体概念板块成分股资金流
try:
    df_members = ak.stock_board_concept_cons_em(symbol="半导体概念")
    log(f"  成分股: {len(df_members)}只")
    for _, r in df_members.iterrows():
        cd = str(r.get('代码', ''))
        if cd in semi_codes:
            log(f"    {r.get('名称','')}({cd}): {r.get('最新价',0):.2f} 涨{r.get('涨跌幅',0):.2f}% "
                f"换手{r.get('换手率',0):.2f}% 市值{r.get('总市值',0)/1e8:.0f}亿")
    results['concept_members'] = df_members.to_dict('records')
except Exception as e:
    log(f"  FAIL: {e}")

# ============================================================
# 9. 北向资金持仓前10
# ============================================================
log("\n" + "="*60)
log("9. 北向资金持仓排名")
try:
    df_north_rank = ak.stock_hsgt_board_rank_em(symbol="北向资金持股排名", 
                                                  indicator="今日")
    if df_north_rank is not None and len(df_north_rank) > 0:
        # 过滤半导体
        semi_north = df_north_rank[df_north_rank['名称'].apply(
            lambda x: any(c in str(x) for c in ['中芯','韦尔','兆易','北方','中微','紫光','寒武',
                                                  '澜起','长电','华天','通富','卓胜','圣邦','斯达',
                                                  '拓荆','长川','沪硅','安集','晶瑞','彤程','华虹']))
        ]
        log(f"  半导体北向持仓: {len(semi_north)}只")
        for _, r in semi_north.iterrows():
            log(f"    {r['名称']}({r['代码']}): 持股市值{r.get('持股市值',0)/1e8:.2f}亿 "
                f"占流通股{r.get('占流通股比例',0):.2f}%")
        results['north_holding'] = semi_north.to_dict('records')
except Exception as e:
    log(f"  FAIL: {e}")

# ============================================================
# 保存
# ============================================================
log("\n" + "="*60)
log("10. 保存数据")

output = {}
for key, val in results.items():
    if isinstance(val, pd.DataFrame):
        output[key] = val.to_dict('records')
    else:
        output[key] = val

with open(os.path.join(OUTPUT_DIR, "akshare_data.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2, default=str)

log(f"\n数据已保存: {OUTPUT_DIR}/akshare_data.json")
log("Done!")
