import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
for f in ['02-proposal.md','10-competition.md','19-consistency.md','06-graph-mhgsl.md','11-compliance.md']:
    t = open(f, encoding='utf-8', errors='replace').read().split('\n')
    print('====', f, len(t), 'lines')
    for i, l in enumerate(t):
        if l.startswith('#'):
            print('  ', i+1, l[:130])
