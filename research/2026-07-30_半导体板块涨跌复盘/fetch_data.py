#!/usr/bin/env python3
"""批量获取A股半导体板块数据：估值、北向资金、龙虎榜、ETF、行情"""
import json
import re
import time
import urllib.request
import urllib.parse
import os
from datetime import datetime, timedelta

OUTPUT_DIR = r"D:\Contents\research\2026-07-30_半导体板块涨跌复盘"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_json(url, retries=3):
    """带重试的JSON获取"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://data.eastmoney.com/'
    }
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                return raw
        except Exception as e:
            if i == retries - 1:
                print(f"FETCH FAILED [{url}]: {e}")
                return None
            time.sleep(1)
    return None

def fetch_raw(url, retries=3):
    """获取原始文本"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read().decode('gbk', errors='ignore')
        except:
            time.sleep(1)
    return None

# ============================================================
# 1. 半导体板块行情数据 - 腾讯API
# ============================================================
print("=" * 60)
print("1. 获取半导体板块行情 (腾讯API)")

# 半导体核心个股列表
SEMI_STOCKS = {
    "设计": ["603501", "300661", "603986", "002049", "300782", "603160", "688256", "688008", "688521", "688536"],
    "制造": ["688981", "688347", "688396"],
    "封测": ["600584", "002185", "002156", "603005"],
    "设备": ["002371", "688012", "688072", "300604"],
    "材料": ["688126", "688019", "300655", "603650", "688200"],
    "EDA/IP": ["688206", "688981"],
    "功率半导体": ["603290", "300623", "688187"],
}

# 构建腾讯行情查询
all_codes = []
for cat, codes in SEMI_STOCKS.items():
    for code in codes:
        if code.startswith('6'):
            all_codes.append(f'sh{code}')
        else:
            all_codes.append(f'sz{code}')

# 分批查询（腾讯API一次最多约50个）
batch_size = 40
stock_data = {}

for i in range(0, len(all_codes), batch_size):
    batch = all_codes[i:i+batch_size]
    url = f"http://qt.gtimg.cn/q={','.join(batch)}"
    raw = fetch_raw(url)
    if raw:
        for line in raw.strip().split('\n'):
            if '~' not in line:
                continue
            parts = line.split('~')
            if len(parts) < 50:
                continue
            try:
                code = parts[2]
                name = parts[1]
                price = float(parts[3]) if parts[3] else 0
                change_pct = float(parts[32]) if parts[32] else 0
                pe = float(parts[39]) if parts[39] else 0
                market_cap = float(parts[45]) if parts[45] else 0  # 流通市值(亿)
                total_market_cap = float(parts[44]) if parts[44] else 0
                turnover = float(parts[37]) if parts[37] else 0  # 成交额(万)
                volume = float(parts[6]) if parts[6] else 0  # 成交量(手)
                high = float(parts[33]) if parts[33] else 0
                low = float(parts[34]) if parts[34] else 0
                open_price = float(parts[5]) if parts[5] else 0
                prev_close = float(parts[4]) if parts[4] else 0
                
                stock_data[code] = {
                    "name": name, "price": price, "change_pct": change_pct,
                    "pe": pe, "market_cap": market_cap, "total_market_cap": total_market_cap,
                    "turnover": turnover, "volume": volume,
                    "high": high, "low": low, "open": open_price, "prev_close": prev_close
                }
            except (ValueError, IndexError) as e:
                continue
    time.sleep(0.3)

print(f"  获取到 {len(stock_data)} 只个股行情")

# 计算板块统计
total_mc = sum(v['total_market_cap'] for v in stock_data.values())
print(f"  板块总市值: {total_mc:.0f}亿")
pe_list = [v['pe'] for v in stock_data.values() if v['pe'] > 0]
if pe_list:
    print(f"  PE范围: {min(pe_list):.1f} ~ {max(pe_list):.1f}, 中位数: {sorted(pe_list)[len(pe_list)//2]:.1f}")

# ============================================================
# 2. 指数行情数据
# ============================================================
print("\n" + "=" * 60)
print("2. 获取指数行情")

# 国证芯片(980017) 和 申万半导体 通过ETF代理
indices = {
    "国证芯片指数": "sz980017",
    "芯片ETF_159995": "sz159995",
    "半导体ETF_512480": "sh512480",
    "科创50": "sh000688",
    "创业板指": "sz399006",
}

index_data = {}
for name, code in indices.items():
    url = f"http://qt.gtimg.cn/q={code}"
    raw = fetch_raw(url)
    if raw:
        for line in raw.strip().split('\n'):
            if '~' not in line:
                continue
            parts = line.split('~')
            try:
                price = float(parts[3]) if parts[3] else 0
                change_pct = float(parts[32]) if parts[32] else 0
                pe = float(parts[39]) if parts[39] else 0
                index_data[name] = {"price": price, "change_pct": change_pct, "pe": pe}
                print(f"  {name}: {price:.2f} ({change_pct:+.2f}%), PE={pe:.1f}")
            except:
                pass
    time.sleep(0.2)

# ============================================================
# 3. 东方财富 - 板块估值数据 (行业板块PE/PB)
# ============================================================
print("\n" + "=" * 60)
print("3. 获取东方财富板块估值数据")

# 东方财富行业板块列表API
sector_url = "http://push2.eastmoney.com/api/qt/clist/get?cb=&fid=f3&po=1&pz=200&pn=1&np=1&fltt=2&invt=2&fields=f2,f3,f4,f12,f14,f9,f20,f21,f23,f115&fs=m:90+t2"
raw = fetch_json(sector_url)
sector_valuation = {}
if raw:
    try:
        data = json.loads(raw)
        if 'data' in data and data['data'] and 'diff' in data['data']:
            for item in data['data']['diff']:
                name = item.get('f14', '')
                if '半导' in name or '芯片' in name:
                    sector_valuation[name] = {
                        "price": item.get('f2', 0),
                        "change_pct": item.get('f3', 0),
                        "pe": item.get('f9', 0),
                        "market_cap": item.get('f20', 0),
                        "pb": item.get('f23', 0),
                    }
                    print(f"  {name}: 涨跌{item.get('f3',0):+.2f}%, PE={item.get('f9',0):.2f}, PB={item.get('f23',0):.2f}")
    except Exception as e:
        print(f"  解析失败: {e}")

# ============================================================
# 4. 东方财富 - 龙虎榜数据 (2026年7月)
# ============================================================
print("\n" + "=" * 60)
print("4. 获取龙虎榜数据 (2026年7月)")

lhb_data = []
# 东方财富龙虎榜API - 按日期查询
for day in range(1, 32):
    date_str = f"2026-07-{day:02d}"
    try:
        dt = datetime(2026, 7, day)
        if dt > datetime.now():
            break
    except:
        break
    
    url = f"http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YYSR&js=var+data=({date_str})&st=1&sr=-1&p=1&ps=500&mkt=1&fd={date_str}"
    raw = fetch_json(url)
    if raw and date_str in raw:
        try:
            # 东方财富龙虎榜用特殊格式
            # 尝试另一种API
            pass
        except:
            pass
    
    # 使用龙虎榜个股明细API
    url2 = f"http://datainterface3.eastmoney.com/EM_DataCenter/JS.aspx?type=GDR&sty=GDR&js=var+data=({date_str})&st=4&sr=-1&p=1&ps=200&mkt=1&fd={date_str}"
    raw2 = fetch_json(url2)
    if raw2 and 'data' in raw2:
        try:
            # 解析...
            pass
        except:
            pass
    
    time.sleep(0.3)

print("  龙虎榜API格式需进一步确认，先跳过")

# ============================================================
# 5. 东方财富 - 北向资金数据
# ============================================================
print("\n" + "=" * 60)
print("5. 获取北向资金数据")

# 北向资金日度数据
north_flow_data = []
for day in range(1, 32):
    date_str = f"2026-07-{day:02d}"
    try:
        dt = datetime(2026, 7, day)
        if dt.weekday() >= 5 or dt > datetime.now():
            continue
    except:
        break
    
    url = f"http://push2his.eastmoney.com/api/qt/kamt.kline/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&klt=101&lmt=1&ut=b2884a393a59ad64002292a3e90d46a5&cb=&begin={date_str}&end={date_str}"
    raw = fetch_json(url)
    if raw:
        try:
            data = json.loads(raw)
            if 'data' in data and data['data']:
                item = data['data']
                north_flow_data.append({
                    "date": date_str,
                    "net_flow": item.get('s2n', 0),  # 北向净流入(亿)
                    "balance": item.get('ye', 0),
                })
        except:
            pass
    time.sleep(0.2)

if north_flow_data:
    total_flow = sum(item['net_flow'] for item in north_flow_data)
    print(f"  7月北向资金累计净流入: {total_flow:.2f}亿 (共{len(north_flow_data)}个交易日)")
    for item in north_flow_data:
        print(f"    {item['date']}: {item['net_flow']:+.2f}亿")

# ============================================================
# 6. 东方财富 - 半导体个股北向持股变化
# ============================================================
print("\n" + "=" * 60)
print("6. 获取北向资金个股持仓")

north_holding = {}
for code, info in list(stock_data.items())[:10]:  # 只查前10只减少请求
    secid = f"1.{code}" if code.startswith('6') else f"0.{code}"
    # 北向持仓API
    url = f"http://push2.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=1&klt=1&secid={secid}&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
    raw = fetch_json(url)
    if raw:
        try:
            data = json.loads(raw)
            if 'data' in data and data['data'] and 'klines' in data['data']:
                klines = data['data']['klines']
                if klines:
                    parts = klines[-1].split(',')
                    north_holding[code] = {
                        "date": parts[0] if len(parts) > 0 else "",
                        "main_net_flow": float(parts[1]) if len(parts) > 1 else 0,  # 主力净流入
                    }
        except:
            pass
    time.sleep(0.3)

# ============================================================
# 7. ETF份额变化数据
# ============================================================
print("\n" + "=" * 60)
print("7. 获取ETF份额变化")

etf_list = [
    ("159995", "芯片ETF(华夏)"),
    ("512480", "半导体ETF(国联安)"),
    ("159813", "半导体ETF(鹏华)"),
    ("588000", "科创50ETF"),
    ("516640", "芯片龙头ETF"),
]

etf_data = {}
for code, name in etf_list:
    secid = f"0.{code}"
    # 尝试获取ETF基金份额
    url = f"http://push2.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20260730&lmt=22&cb="
    raw = fetch_json(url)
    if raw:
        try:
            data = json.loads(raw)
            if 'data' in data and data['data'] and 'klines' in data['data']:
                klines = data['data']['klines']
                # 提取7月数据
                july_data = []
                for k in klines:
                    parts = k.split(',')
                    date = parts[0]
                    if '2026-07' in date:
                        july_data.append({
                            "date": date,
                            "open": float(parts[1]),
                            "close": float(parts[2]),
                            "high": float(parts[3]),
                            "low": float(parts[4]),
                            "volume": float(parts[5]),
                            "amount": float(parts[6]),
                        })
                etf_data[code] = {"name": name, "july": july_data}
                if july_data:
                    print(f"  {name} ({code}): 7月{len(july_data)}个交易日, "
                          f"最新收盘: {july_data[-1]['close']:.3f}")
        except Exception as e:
            print(f"  {name} 解析失败: {e}")
    time.sleep(0.2)

# ============================================================
# 8. 主力资金流向 (东方财富 - 个股资金流向)
# ============================================================
print("\n" + "=" * 60)
print("8. 获取主力资金流向")

# 半导体板块主力资金
main_flow_url = "http://push2.eastmoney.com/api/qt/clist/get?cb=&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124&fs=b:bk0467"
raw = fetch_json(main_flow_url)
main_flow_stocks = []
if raw:
    try:
        data = json.loads(raw)
        if 'data' in data and data['data'] and 'diff' in data['data']:
            for item in data['data']['diff']:
                main_flow_stocks.append({
                    "code": item.get('f12', ''),
                    "name": item.get('f14', ''),
                    "price": item.get('f2', 0),
                    "change_pct": item.get('f3', 0),
                    "main_net_flow": item.get('f62', 0),  # 主力净流入(万)
                    "main_flow_ratio": item.get('f184', 0),  # 主力净流入占比
                    "super_large_net": item.get('f66', 0),  # 超大单净流入
                    "large_net": item.get('f72', 0),  # 大单净流入
                    "medium_net": item.get('f78', 0),  # 中单净流入
                    "small_net": item.get('f84', 0),  # 小单净流入
                })
        print(f"  获取到 {len(main_flow_stocks)} 只个股主力资金数据")
        # Top 主力净流入前5
        sorted_by_flow = sorted(main_flow_stocks, key=lambda x: x['main_net_flow'], reverse=True)
        print("  主力净流入 Top5:")
        for s in sorted_by_flow[:5]:
            print(f"    {s['name']}({s['code']}): {s['main_net_flow']/10000:.2f}亿, 涨跌{s['change_pct']:+.2f}%")
        print("  主力净流出 Top5:")
        for s in sorted_by_flow[-5:]:
            print(f"    {s['name']}({s['code']}): {s['main_net_flow']/10000:.2f}亿, 涨跌{s['change_pct']:+.2f}%")
    except Exception as e:
        print(f"  解析失败: {e}")

# ============================================================
# 9. 板块日K线数据 (近3个月)
# ============================================================
print("\n" + "=" * 60)
print("9. 获取半导体板块K线数据")

# 申万半导体指数 BK0467
semi_index_url = "http://push2his.eastmoney.com/api/qt/stock/kline/get?secid=90.BK0467&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20260730&lmt=66&cb="
raw = fetch_json(semi_index_url)
semi_index_kline = []
if raw:
    try:
        data = json.loads(raw)
        if 'data' in data and data['data'] and 'klines' in data['data']:
            for k in data['data']['klines']:
                parts = k.split(',')
                semi_index_kline.append({
                    "date": parts[0],
                    "open": float(parts[1]),
                    "close": float(parts[2]),
                    "high": float(parts[3]),
                    "low": float(parts[4]),
                    "volume": float(parts[5]),
                    "amount": float(parts[6]),
                })
            july_k = [x for x in semi_index_kline if '2026-07' in x['date']]
            if july_k:
                july_start = july_k[0]['close']
                july_end = july_k[-1]['close']
                july_high = max(x['high'] for x in july_k)
                july_low = min(x['low'] for x in july_k)
                print(f"  7月半导体板块: 开{july_k[0]['open']:.0f} 收{july_end:.0f} "
                      f"高{july_high:.0f} 低{july_low:.0f}")
                print(f"  7月涨幅: {(july_end/july_k[0]['open']-1)*100:+.2f}%")
                print(f"  7月振幅: {(july_high/july_low-1)*100:.2f}%")
                
                # 每日涨跌
                for kd in july_k:
                    chg = (kd['close']/kd['open']-1)*100
                    print(f"    {kd['date']}: O{kd['open']:.0f} C{kd['close']:.0f} "
                          f"H{kd['high']:.0f} L{kd['low']:.0f} 振幅{(kd['high']/kd['low']-1)*100:.1f}%")
    except Exception as e:
        print(f"  解析失败: {e}")

# ============================================================
# 10. 龙虎榜数据 (使用东方财富LHB API)
# ============================================================
print("\n" + "=" * 60)
print("10. 获取龙虎榜详细数据")

# 东方财富龙虎榜API
lhb_url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YYSR&js=var%20data={pages:(pc),data:[(x)]}&ps=200&p=1&mkt=1&fd=2026-07-01&sr=-1&st=1&rt=53658444"
raw = fetch_json(lhb_url)
lhb_records = []
if raw:
    try:
        # 提取JSON部分
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            if 'data' in data:
                records = data['data']
                semi_lhb = []
                semi_codes_set = set(stock_data.keys())
                for r in records:
                    code = str(r.get('Code', ''))
                    if code in semi_codes_set:
                        semi_lhb.append(r)
                print(f"  龙虎榜总记录: {len(records)}条, 半导体相关: {len(semi_lhb)}条")
                for r in semi_lhb[:20]:
                    print(f"    {r.get('Name','')}({r.get('Code','')}) {r.get('TDate','')}: "
                          f"涨跌{r.get('Chgradio',0):+.2f}% 净买额{r.get('JmMoney',0)/10000:.2f}万")
    except Exception as e:
        print(f"  解析失败: {e}")

# ============================================================
# 11. 保存原始数据
# ============================================================
print("\n" + "=" * 60)
print("11. 保存数据到JSON")

output_data = {
    "fetch_time": datetime.now().isoformat(),
    "stocks": stock_data,
    "indices": index_data,
    "sector_valuation": sector_valuation,
    "north_flow": north_flow_data,
    "etf_data": etf_data,
    "main_flow": main_flow_stocks,
    "semi_index_kline": semi_index_kline,
    "semi_stocks_by_category": SEMI_STOCKS,
}

with open(os.path.join(OUTPUT_DIR, "raw_data.json"), "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2, default=str)

print(f"数据已保存到: {OUTPUT_DIR}/raw_data.json")
print(f"共 {len(stock_data)} 只个股, {len(north_flow_data)} 天北向数据, {len(main_flow_stocks)} 条主力资金")

# 打印板块汇总
print("\n" + "=" * 60)
print("板块数据汇总")
for cat, codes in SEMI_STOCKS.items():
    cat_stocks = {c: stock_data[c] for c in codes if c in stock_data}
    if cat_stocks:
        cat_pe = [v['pe'] for v in cat_stocks.values() if v['pe'] > 0]
        cat_chg = [v['change_pct'] for v in cat_stocks.values()]
        cat_mc = sum(v['total_market_cap'] for v in cat_stocks.values())
        print(f"  {cat}: {len(cat_stocks)}只, 市值{cat_mc:.0f}亿, "
              f"PE中位{sorted(cat_pe)[len(cat_pe)//2]:.1f}" if cat_pe else f"  {cat}: {len(cat_stocks)}只, 市值{cat_mc:.0f}亿",
              f", 涨跌中位{sorted(cat_chg)[len(cat_chg)//2]:+.2f}%")

print("\nDone!")
