import React, { useEffect, useState, useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Info } from 'lucide-react';

/**
 * Fraud Ring Visualization
 * Implements a force-directed graph to visualize fraudulent clusters.
 *
 * Multi-channel visualization:
 * - Topology (T): Structural connections (e.g., same address)
 * - Feature (F): Behavioral similarities (e.g., high frequency)
 * - Semantic (S): Domain-specific relations (e.g., referral chain)
 */

// Palette following dataviz skill for categorical identities
const CHANNEL_COLORS = {
  T: '#2a78d6', // Blue - Topology
  F: '#eb6834', // Orange - Feature
  S: '#1baf7a', // Aqua - Semantic
};

const NODE_COLORS = {
  Provider: '#4a3aa7', // Violet
  Patient: '#008300',  // Green
  Claim: '#e34948',    // Red
};

interface GraphNode {
  id: string;
  label: string;
  type: 'Provider' | 'Patient' | 'Claim';
  riskScore: number;
  contribution: {
    T: number;
    F: number;
    S: number;
  };
}

interface GraphEdge {
  source: string;
  target: string;
  type: 'T' | 'F' | 'S';
  weight: number;
  relation: string;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphEdge[];
}

export default function FraudRing({ claimId }: { claimId: string }) {
  const [data, setData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hoverNode, setHoverNode] = useState<GraphNode | null>(null);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const response = await fetch(`/api/graph/ring/${claimId}`);
        if (!response.ok) throw new Error(`Error fetching graph data: ${response.statusText}`);
        const result = await response.json();
        setData(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [claimId]);

  const graphData = useMemo(() => {
    if (!data) return { nodes: [], links: [] };
    return {
      nodes: data.nodes,
      links: data.links,
    };
  }, [data]);

  if (loading) return <div className="flex items-center justify-center h-full min-h-[400px]">Loading Fraud Ring...</div>;
  if (error) return <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>;
  if (!data) return null;

  return (
    <Card className="w-full h-full flex flex-col overflow-hidden bg-background">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
        <CardTitle className="text-xl font-bold">Fraud Ring Analysis</CardTitle>
        <Badge variant="outline" className="bg-yellow-100 text-yellow-800 border-yellow-300 dark:bg-yellow-900 dark:text-yellow-200 dark:border-yellow-700">
          DATA SINTETIS
        </Badge>
      </CardHeader>
      <CardContent className="flex-1 relative min-h-[600px]">
        <ForceGraph2D
          graphData={graphData}
          nodeLabel="label"
          nodeVal={(node: GraphNode) => Math.max(2, node.riskScore * 2)}
          nodeColor={(node: GraphNode) => NODE_COLORS[node.type] || '#ccc'}
          linkColor={(link: GraphEdge) => CHANNEL_COLORS[link.type] || '#ccc'}
          linkWidth={(link: GraphEdge) => Math.max(1, link.weight)}
          onNodeHover={(node: any) => setHoverNode(node)}
          nodeCanvasObject={(node: any, ctx, globalScale) => {
            const size = node.val * globalScale;
            const label = node.label;

            ctx.beginPath();
            ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
            ctx.fillStyle = node.color;
            ctx.fill();

            if (globalScale > 1.5) {
              ctx.font = `${6 * globalScale}px Inter, system-ui, sans-serif`;
              ctx.textAlign = 'center';
              ctx.textBaseline = 'middle';
              ctx.fillStyle = 'currentColor';
              ctx.fillText(label, node.x, node.y + size + 4);
            }
          }}
          cooldownTicks={100}
        />

        {hoverNode && (
          <div className="absolute top-4 right-4 p-4 bg-popover text-popover-foreground border rounded-lg shadow-lg z-10 w-64 pointer-events-none">
            <div className="font-bold text-lg mb-1">{hoverNode.label}</div>
            <div className="text-sm opacity-70 mb-3">ID: {hoverNode.id}</div>

            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs font-medium">Risk Score:</span>
                <span className="text-sm font-bold">{hoverNode.riskScore.toFixed(2)}</span>
              </div>

              <div className="pt-2 border-t">
                <div className="text-xs font-bold uppercase tracking-wider mb-2 opacity-60">Channel Contribution</div>
                <div className="grid grid-cols-3 gap-2 text-center text-[10px]">
                  <div className="flex flex-col items-center">
                    <div className="w-2 h-2 rounded-full mb-1" style={{ backgroundColor: CHANNEL_COLORS.T }} />
                    <span>T: {hoverNode.contribution.T.toFixed(2)}</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="w-2 h-2 rounded-full mb-1" style={{ backgroundColor: CHANNEL_COLORS.F }} />
                    <span>F: {hoverNode.contribution.F.toFixed(2)}</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="w-2 h-2 rounded-full mb-1" style={{ backgroundColor: CHANNEL_COLORS.S }} />
                    <span>S: {hoverNode.contribution.S.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="absolute bottom-4 left-4 p-3 bg-background/80 backdrop-blur border rounded-md text-xs space-y-2">
          <div className="font-semibold mb-1">Legend</div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: NODE_COLORS.Provider }} /> <span>Provider</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: NODE_COLORS.Patient }} /> <span>Patient</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: NODE_COLORS.Claim }} /> <span>Claim</span>
          </div>
          <div className="pt-2 border-t mt-2"></div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-1 rounded-full" style={{ backgroundColor: CHANNEL_COLORS.T }} /> <span>Topology (T)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-1 rounded-full" style={{ backgroundColor: CHANNEL_COLORS.F }} /> <span>Feature (F)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-1 rounded-full" style={{ backgroundColor: CHANNEL_COLORS.S }} /> <span>Semantic (S)</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
