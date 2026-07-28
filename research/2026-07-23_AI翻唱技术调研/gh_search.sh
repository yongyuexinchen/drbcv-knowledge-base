#!/bin/bash
TOKEN=$(grep 'github.com' ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
PROXY="http://127.0.0.1:7897"
AUTH="Authorization: token $TOKEN"
BASE="https://api.github.com/search/repositories"

search_gh() {
  local cat="$1" q="$2"
  local url="${BASE}?q=$(echo "$q" | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))")&sort=stars&order=desc&per_page=3"
  curl -s --max-time 15 --proxy "$PROXY" -H "$AUTH" "$url"
}

echo "=== RVC ==="
search_gh "RVC" "RVC voice conversion webui" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for i in d.get('items',[])[:3]:
  print(f\"{i['full_name']}|{i['html_url']}|{i['stargazers_count']}|{i.get('language','')}|{i.get('description','')}|{i.get('updated_at','')}|{i.get('forks_count',0)}|{i.get('open_issues_count',0)}|{i.get('license',{}).get('spdx_id','') if i.get('license') else ''}\")
"

echo "=== so-vits-svc ==="
search_gh "SoVITS" "so-vits-svc" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for i in d.get('items',[])[:3]:
  print(f\"{i['full_name']}|{i['html_url']}|{i['stargazers_count']}|{i.get('language','')}|{i.get('description','')}|{i.get('updated_at','')}|{i.get('forks_count',0)}|{i.get('open_issues_count',0)}|{i.get('license',{}).get('spdx_id','') if i.get('license') else ''}\")
"

echo "=== GPT-SoVITS ==="
search_gh "GPT-SoVITS" "GPT-SoVITS" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for i in d.get('items',[])[:3]:
  print(f\"{i['full_name']}|{i['html_url']}|{i['stargazers_count']}|{i.get('language','')}|{i.get('description','')}|{i.get('updated_at','')}|{i.get('forks_count',0)}|{i.get('open_issues_count',0)}|{i.get('license',{}).get('spdx_id','') if i.get('license') else ''}\")
"
