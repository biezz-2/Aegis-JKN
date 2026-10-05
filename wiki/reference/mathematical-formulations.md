---
title: Mathematical Formulations
type: reference
tags: [math, formulas, gcn, cosine, attention, sigmoid, latex]
related:
  - "[[overview]]"
  - "[[concepts/mhgsl-architecture]]"
sources:
  - src/components/mhgsl/math-formulas.tsx
---

# Formulasi Matematis Arsitektur MHGSL

## 1. Saluran Graf Fitur: Matriks Kedekatan Kosinus (*Cosine Adjacency*)

Untuk pasangan entitas $i$ dan $j$ dengan vektor fitur atribut $x_i, x_j \in \mathbb{R}^d$:

$$A_{ij}^{(\text{feat})} = \begin{cases} \dfrac{x_i \cdot x_j}{\|x_i\| \|x_j\|} & \text{jika } \dfrac{x_i \cdot x_j}{\|x_i\| \|x_j\|} \ge \epsilon \\ 0 & \text{lainnya} \end{cases}$$

Di mana $\epsilon \in (0, 1)$ adalah ambang batas sparsity untuk mempertahankan edge berbobot signifikan saja.

## 2. Channel-Specific Graph Convolutional Network (GCN)

Untuk saluran $c \in \{\text{topo}, \text{feat}, \text{sem}\}$, propagasi pesan lapisan ke-$(l+1)$ dirumuskan sebagai:

$$H_c^{(l+1)} = \text{ReLU}\left( \tilde{D}_c^{-\frac{1}{2}} \tilde{A}_c \tilde{D}_c^{-\frac{1}{2}} H_c^{(l)} W_c^{(l)} \right)$$

Di mana:
- $\tilde{A}_c = A_c + I_N$ adalah matriks ketetanggaan dengan *self-loop*.
- $\tilde{D}_{c,ii} = \sum_j \tilde{A}_{c,ij}$ adalah matriks derajat diagonal.
- $W_c^{(l)}$ adalah matriks bobot yang dapat dipelajari khusus untuk saluran $c$.

## 3. Shared-Parameter GCN (Weight Sharing)

Untuk mengekstraksi struktur invarian lintas saluran:

$$Z_c = \text{ReLU}\left( \tilde{D}_c^{-\frac{1}{2}} \tilde{A}_c \tilde{D}_c^{-\frac{1}{2}} H_c^{(L)} W_{\text{shared}} \right)$$

Di mana $W_{\text{shared}}$ digunakan bersama oleh semua saluran untuk menyelaraskan ruang embedding laten.

## 4. Adaptive Attention Fusion & Klasifikasi Sigmoid

Bobot atensi terbobot untuk saluran $c$:

$$e_c = q^T \tanh\left( W_{\text{att}} Z_c + b_{\text{att}} \right)$$

$$\alpha_c = \frac{\exp(e_c)}{\sum_{c'} \exp(e_{c'})}$$

Representasi akhir hasil fusi $Z_{\text{fused}}$:

$$Z_{\text{fused}} = \sum_{c} \alpha_c Z_c$$

Probabilitas prediksi fraud akhir:

$$\hat{y} = \sigma\left( W_{\text{out}} Z_{\text{fused}} + b_{\text{out}} \right) \in [0, 1]$$
