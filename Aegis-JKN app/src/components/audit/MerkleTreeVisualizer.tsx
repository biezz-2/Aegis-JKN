'use client';

import React, { useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, XCircle, Info, GitBranch } from 'lucide-react';

interface MerkleTreeVisualizerProps {
  leafHashes: string[];
  rootHash: string;
  verified: boolean;
}

export function MerkleTreeVisualizer({ leafHashes, rootHash, verified }: MerkleTreeVisualizerProps) {
  // We simulate the tree structure for visualization
  const tree = useMemo(() => {
    let currentLayer = leafHashes;
    const layers: string[][] = [currentLayer];

    while (currentLayer.length > 1) {
      const nextLayer: string[] = [];
      for (let i = 0; i < currentLayer.length; i += 2) {
        const left = currentLayer[i];
        const right = currentLayer[i + 1] || left;
        // Mock hash combination for visualization
        nextLayer.push(`hash(${left.slice(0,4)}..${right.slice(0,4)}..)`);
      }
      currentLayer = nextLayer;
      layers.push(currentLayer);
    }
    return layers;
  }, [leafHashes]);

  return (
    <Card className="w-full overflow-hidden bg-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <GitBranch className="h-5 w-5 text-primary" />
              Cryptographic Proof (Merkle Tree)
            </CardTitle>
            <CardDescription>
              Visualization of the immutable log anchor. Root hash represents the entire dataset state.
            </CardDescription>
          </div>
          <Badge variant={verified ? 'default' : 'destructive'} className="gap-1">
            {verified ? <CheckCircle2 className="h-3 w-3" /> : <XCircle className="h-3 w-3" />}
            {verified ? 'Root Verified' : 'Invalid Root'}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col items-center gap-8 py-12">
        <div className="flex flex-col-reverse gap-8 w-full items-center">
          {tree.map((layer, layerIdx) => (
            <div key={layerIdx} className="flex justify-center gap-4 w-full">
              {layer.map((hash, nodeIdx) => (
                <div
                  key={nodeIdx}
                  className={`px-3 py-1 rounded border text-[10px] font-mono transition-all
                    ${layerIdx === tree.length - 1
                      ? 'bg-primary text-primary-foreground border-primary font-bold'
                      : 'bg-muted text-muted-foreground border-border'}
                    ${verified ? 'ring-1 ring-green-500/30' : 'ring-1 ring-red-500/30'}
                  `}
                >
                  {hash.length > 12 ? `${hash.slice(0, 8)}...${hash.slice(-4)}` : hash}
                </div>
              ))}
            </div>
          ))}
        </div>

        <div className="bg-muted/50 p-4 rounded-lg border border-border max-w-2xl w-full flex items-start gap-3 text-sm">
          <Info className="h-5 w-5 text-primary shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="font-semibold">How it works</p>
            <p className="text-muted-foreground text-xs">
              Each log entry is a leaf. Pairs are hashed recursively until a single <strong>Root Hash</strong> is reached.
              If any single byte in any log entry changes, the Root Hash will change completely.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono p-2 bg-background border rounded-md">
          <span className="text-muted-foreground">Anchor Root:</span>
          <span className="font-bold">{rootHash || 'Not Generated'}</span>
        </div>
      </CardContent>
    </Card>
  );
}