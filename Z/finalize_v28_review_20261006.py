import hashlib
import json
import re
import shutil
import statistics
from pathlib import Path

reports = Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\result\innovation2\TOPOLOGY_V28')
mirror = Path(r'E:\Z\result\innovation2\TOPOLOGY_V28')
current_path = Path(r'E:\Z\v28_review_current_state_20261006.json')
current = json.loads(current_path.read_text(encoding='utf-8-sig'))
read = lambda n: json.loads((reports / n).read_text(encoding='utf-8-sig'))
a = read('06_PHASE_A_METRICS.json')
b = read('11_PHASE_B_NEW_SEED_RESULTS.json')
verified = 0
for data in (a, b['new_seeds_only'], b['all_eight_seeds']):
    for ds, dataset in data['datasets'].items():
        for name, effects in dataset['effects'].items():
            candidate, control = name.split('_vs_')
            for metric, direction in (('ce', -1), ('mrr', 1)):
                vals = [direction * (r['arms'][candidate]['validation'][metric] - r['arms'][control]['validation'][metric])
                        for r in dataset['seed_results']]
                e = effects[metric]
                assert abs(statistics.mean(vals) - e['mean']) < 1e-12, (ds, name, metric)
                assert sum(v > 0 for v in vals) == e['wins'], (ds, name, metric, 'wins')
                assert all(abs(x-y) < 1e-12 for x,y in zip(vals, e['per_seed'])), (ds, name, metric, 'seed')
                verified += 1
for name, record in current['report_files'].items():
    local = reports / name
    if local.is_file():
        assert hashlib.sha256(local.read_bytes()).hexdigest() == record['sha256'], name
assert not current['live_python_trainers']
assert current['inner_training_result_count'] == 0
assert all(c['test_flags'] and all(v is False for k,v in c['test_flags']) for c in current['raw_result_records'])
current['local_server_existing_report_hashes_match'] = True
current['recomputed_paired_metric_groups'] = verified
current['review_complete'] = True
current['v28_experiments_complete'] = False
current['test_opened'] = False
current['review_client_date'] = '2026-10-06'
current['review_client_timezone'] = 'America/Los_Angeles'

p = reports / 'V28_FINAL_RESEARCH_REVIEW.md'
text = p.read_text(encoding='utf-8')
text = text.replace('STATUS: REVIEWED  \nWORKSPACE:', 'STATUS: REVIEWED  \nREVIEW_COMPLETE: YES  \nREVIEW_UPDATED: 2026-10-06 (America/Los_Angeles)  \nWORKSPACE:', 1)
text = text.replace('服务器根分区219G、可用0、占用100%。因此', '失败发生时服务器根分区219G、可用0、占用100%。因此')
text = text.replace('当前没有topology28.py或resume_inner28.py进程，GPU0%、14MiB。', '本次2026-10-06复核未发现Python训练进程。')
text = text.replace('本次审查没有修复服务器、清理磁盘、续跑训练或改写这些状态。', '这些历史结果与状态文件保持原样。磁盘已按用户另外授权完成备份与清理；恢复可用空间本身不构成未执行实验的结果。')
text = text.replace("| 冻结源码/历史缓存 | 哈希失败0 | 创新点1、历史源文件与V27特征未改动。 |", "| 冻结源码/历史缓存 | 清理前审查记录哈希失败0 | 历史源码与缓存已归档到本地；这是清理前证据，不代表本次仍可在服务器逐项读取。 |")
section = f'''### 1.3 最终审查完成确认（2026-10-06）

**REVIEW_COMPLETE: YES；V28_COMPLETE: NO。** 本报告完成用户要求的A–E项及六个决策问题；V28原实验计划缺失内部融合验证和5/10epoch稳定性，不能报告为实验全部完成。

已只读读取服务器当前155份原始日志及128份原始结果记录（训练记录与backbone记录合计）；128份均有test封存字段，且全部为false。内部融合训练结果0份，内部backbone结果6份。所有本地现存报告对应服务器文件的SHA-256一致，原Phase A、新种子3–7及全部8种子的{verified}组配对CE/MRR均由逐种子原始指标重算通过。此前118个规范结果单元的checkpoint/score/CE检查仍采用清理前审查记录；它和本次128份原始记录的计数范围不同。

服务器目前约{current['disk_available_bytes']/1024**3:.2f} GiB可用；V28目录及原始数据集保留。历史实验依赖源码和缓存已在用户授权的空间清理中从服务器移除，完整副本保存在 `E:/Z/DCDLP_Server_Backup_20261005/lchr_v2_full_server_backup.tar.gz`。本报告不改变历史指标、训练状态或创新点1；没有重新训练或执行V29。

本次当前状态证据见 [V28_FINAL_REVIEW_CURRENT_STATE.json](V28_FINAL_REVIEW_CURRENT_STATE.json)，清理前完整性审查见 [V28_FINAL_REVIEW_EVIDENCE_AUDIT.json](V28_FINAL_REVIEW_EVIDENCE_AUDIT.json)。`workspace_info`在当前可用工具中不存在，工作区身份由WORKSPACE_AUDIT和实际本地/服务器项目路径核对确认，不能声称已调用不存在的工具。

'''
text = text.replace('## 2. 已完成的Phase A：全部方法', section + '## 2. 已完成的Phase A：全部方法', 1)
text = re.sub(r'\]\(([A-Za-z0-9_]+\.(?:md|json|log))\)', lambda m: '](' + (reports / m.group(1)).as_posix() + ')', text)
required = ('GRAPH_STATUS: EXPLORATORY', 'MULT_STATUS: EXPLORATORY',
            'GRAPH_MULT_STATUS: UNRESOLVED', 'HDP_CONDITIONAL_STATUS: EXPLORATORY',
            'NEXT_EXPECTED_STEP: WAIT_FOR_REVIEW', 'V28_COMPLETE: NO', 'TEST_OPENED: NO')
assert all(x in text for x in required)
p.write_text(text, encoding='utf-8')
(reports / 'V28_FINAL_REVIEW_CURRENT_STATE.json').write_text(json.dumps(current, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
shutil.copy2(Path(r'E:\Z\v28_review_audit.json'), reports / 'V28_FINAL_REVIEW_EVIDENCE_AUDIT.json')
mirror.mkdir(parents=True, exist_ok=True)
for name in ('V28_FINAL_RESEARCH_REVIEW.md', 'V28_FINAL_REVIEW_CURRENT_STATE.json', 'V28_FINAL_REVIEW_EVIDENCE_AUDIT.json'):
    shutil.copy2(reports / name, mirror / name)
print(json.dumps({'report':str(p), 'mirror':str(mirror / p.name), 'paired_metric_checks':verified,
                  'review_complete':True, 'experiments_complete':False}, ensure_ascii=False))
