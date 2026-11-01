import { createHash } from 'node:crypto';

/**
 * Cryptographic utilities for Audit Trail Immutability
 */

export function calculateAuditHash(entry: any): string {
  const data = `${entry.timestamp}|${entry.claimId}|${entry.eventType}|${JSON.stringify(entry.payload)}|${entry.previousHash}`;
  return createHash('sha256').update(data).digest('hex');
}

export function verifyHashChain(entries: any[]): { isValid: boolean; errorIndex?: number } {
  for (let i = 1; i < entries.length; i++) {
    const current = entries[i];
    const previous = entries[i - 1];

    if (current.previousHash !== previous.hash) {
      return { isValid: false, errorIndex: i };
    }

    if (current.hash !== calculateAuditHash(current)) {
      return { isValid: false, errorIndex: i };
    }
  }
  return { isValid: true };
}

/**
 * Merkle Tree Implementation for Efficient Verification
 */
export function buildMerkleRoot(leafHashes: string[]): string {
  if (leafHashes.length === 0) return '';

  let currentLayer = leafHashes;

  while (currentLayer.length > 1) {
    const nextLayer: string[] = [];
    for (let i = 0; i < currentLayer.length; i += 2) {
      const left = currentLayer[i];
      const right = currentLayer[i + 1] || left; // Duplicate last leaf if odd
      const combinedHash = createHash('sha256').update(left + right).digest('hex');
      nextLayer.push(combinedHash);
    }
    currentLayer = nextLayer;
  }

  return currentLayer[0];
}

export function generateDigitalSignature(data: string): string {
  // Mock digital signature for demo purposes
  return createHash('sha256').update(data + 'SECRET_KEY').digest('hex');
}