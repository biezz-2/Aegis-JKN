/*
 * Aegis-JKN landing — charts.
 *
 * Two horizontal bar charts, hand-built SVG. No dependencies.
 * Colours are the validated categorical slots 1–3 (see landing.css --series-*);
 * the score chart uses the reserved status palette because a triage queue *is* a
 * state (good / warning / critical) and each one ships with a written label.
 *
 * Every value shown in a chart is also present in the page's table view, so the
 * tooltip and the hover layer enhance rather than gate.
 */
(function () {
	'use strict';

	var SVG_NS = 'http://www.w3.org/2000/svg';

	var CHANNEL = {
		series: [
			{ name: 'Topologi (A_top)', color: '#3987e5' },
			{ name: 'Fitur (A_feat)', color: '#d95926' },
			{ name: 'Semantik (A_sem)', color: '#199e70' }
		],
		groups: [
			{
				label: 'Auto-clear',
				n: 240,
				note: 'klaim normal, lolos otomatis',
				values: [0.033, 0.03, 0.024]
			},
			{
				label: 'Review',
				n: 24,
				note: 'anomali sedang, telaah verifikator',
				values: [0.155, 0.201, 0.163]
			},
			{
				label: 'Escalate',
				n: 36,
				note: 'anomali tinggi, indikasi sindikat',
				values: [0.265, 0.305, 0.293]
			}
		],
		max: 0.35,
		ticks: [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
	};

	var SCORE = {
		groups: [
			{
				label: 'Auto-clear',
				n: 240,
				mean: 0.086,
				min: 0.04,
				max: 0.14,
				value: 'Rp 2.685.550.000',
				color: '#0ca30c',
				state: 'rendah'
			},
			{
				label: 'Review',
				n: 24,
				mean: 0.591,
				min: 0.4,
				max: 0.79,
				value: 'Rp 279.950.000',
				color: '#fab219',
				state: 'sedang'
			},
			{
				label: 'Escalate',
				n: 36,
				mean: 0.869,
				min: 0.8,
				max: 0.95,
				value: 'Rp 561.150.000',
				color: '#d03b3b',
				state: 'tinggi'
			}
		],
		max: 1,
		ticks: [0, 0.2, 0.4, 0.6, 0.8, 1]
	};

	/* ---------- helpers ---------- */

	function fmt(n, digits) {
		return n.toLocaleString('id-ID', {
			minimumFractionDigits: digits,
			maximumFractionDigits: digits
		});
	}

	function el(name, attrs, parent) {
		var node = document.createElementNS(SVG_NS, name);
		for (var key in attrs) {
			if (Object.prototype.hasOwnProperty.call(attrs, key)) {
				node.setAttribute(key, attrs[key]);
			}
		}
		if (parent) parent.appendChild(node);
		return node;
	}

	function text(parent, x, y, str, cls, extra) {
		var node = el('text', { x: x, y: y, class: cls }, parent);
		node.textContent = str;
		if (extra) {
			for (var key in extra) {
				if (Object.prototype.hasOwnProperty.call(extra, key)) {
					node.style[key] = extra[key];
				}
			}
		}
		return node;
	}

	/* Bar anchored at the baseline on the left, 4px rounded at the data end. */
	function barPath(x, y, w, h, r) {
		var len = Math.max(w, 0.6);
		r = Math.min(r, len, h / 2);
		if (len <= r + 0.5) {
			return 'M' + x + ',' + y + ' h' + len + ' v' + h + ' h' + -len + ' Z';
		}
		return (
			'M' + x + ',' + y +
			' h' + (len - r) +
			' a' + r + ',' + r + ' 0 0 1 ' + r + ',' + r +
			' v' + (h - 2 * r) +
			' a' + r + ',' + r + ' 0 0 1 ' + -r + ',' + r +
			' h' + -(len - r) + ' Z'
		);
	}

	/* Floating bar — both ends are data ends, so both are rounded. */
	function rangePath(x, y, w, h, r) {
		var len = Math.max(w, 0.6);
		r = Math.min(r, len / 2, h / 2);
		return (
			'M' + (x + r) + ',' + y +
			' h' + (len - 2 * r) +
			' a' + r + ',' + r + ' 0 0 1 ' + r + ',' + r +
			' v' + (h - 2 * r) +
			' a' + r + ',' + r + ' 0 0 1 ' + -r + ',' + r +
			' h' + -(len - 2 * r) +
			' a' + r + ',' + r + ' 0 0 1 ' + -r + ',' + -r +
			' v' + -(h - 2 * r) +
			' a' + r + ',' + r + ' 0 0 1 ' + r + ',' + -r + ' Z'
		);
	}

	/* ---------- tooltip ---------- */

	function Tooltip(holder) {
		this.node = document.createElement('div');
		this.node.className = 'chart-tooltip';
		this.node.setAttribute('role', 'status');
		this.node.setAttribute('aria-live', 'polite');
		holder.appendChild(this.node);
	}

	Tooltip.prototype.show = function (x, y, title, rows) {
		var node = this.node;
		node.textContent = '';

		var head = document.createElement('div');
		head.className = 'tt-title';
		head.textContent = title;
		node.appendChild(head);

		for (var i = 0; i < rows.length; i++) {
			var row = document.createElement('div');
			row.className = 'tt-row';

			if (rows[i].color) {
				var key = document.createElement('span');
				key.style.width = '10px';
				key.style.height = '2px';
				key.style.borderRadius = '1px';
				key.style.background = rows[i].color;
				key.style.flexShrink = '0';
				row.appendChild(key);
			}

			var val = document.createElement('strong');
			val.textContent = rows[i].value;
			row.appendChild(val);

			var lab = document.createElement('span');
			lab.textContent = rows[i].label;
			row.appendChild(lab);

			node.appendChild(row);
		}

		node.classList.add('visible');

		// Keep the tooltip inside the holder.
		var hw = this.node.offsetWidth;
		var hh = this.node.offsetHeight;
		var maxX = holder.clientWidth - hw - 4;
		var left = Math.max(4, Math.min(x + 12, maxX));
		var top = Math.max(4, y - hh - 10);
		this.node.style.left = left + 'px';
		this.node.style.top = top + 'px';
	};

	Tooltip.prototype.hide = function () {
		this.node.classList.remove('visible');
	};

	/* ---------- chart 1: channel contribution by triage queue ---------- */

	function renderChannel(holder, tip) {
		var W = holder.clientWidth;
		if (!W) return;

		var PAD = { top: 6, right: 66, bottom: 34, left: 148 };
		var BAR = 22;
		var GAP = 2;
		var GROUP_GAP = 26;
		var HEAD = 30;

		var groups = CHANNEL.groups;
		var plotW = W - PAD.left - PAD.right;
		var bodyH = 0;
		for (var g = 0; g < groups.length; g++) {
			bodyH += HEAD + CHANNEL.series.length * BAR + (CHANNEL.series.length - 1) * GAP;
		}
		bodyH += (groups.length - 1) * GROUP_GAP;

		var H = PAD.top + bodyH + PAD.bottom;

		var svg = el('svg', {
			viewBox: '0 0 ' + W + ' ' + H,
			width: W,
			height: H,
			role: 'img',
			'aria-label':
				'Rata-rata kontribusi kanal per antrean triase. Auto-clear 0,033 topologi, 0,030 fitur, ' +
				'0,024 semantik. Review 0,155, 0,201, 0,163. Escalate 0,265, 0,305, 0,293. ' +
				'Nilai lengkap tersedia pada tabel di bawah grafik.'
		}, holder);
		svg.setAttribute('class', 'chart-svg');

		var x = function (v) {
			return PAD.left + (v / CHANNEL.max) * plotW;
		};

		// gridlines + x axis
		for (var t = 0; t < CHANNEL.ticks.length; t++) {
			var tv = CHANNEL.ticks[t];
			var gx = x(tv);
			el('line', {
				x1: gx, y1: PAD.top, x2: gx, y2: PAD.top + bodyH,
				class: tv === 0 ? 'axis-line' : 'grid-line'
			}, svg);
			text(svg, gx, PAD.top + bodyH + 18, fmt(tv, 2), 'axis-text', {
				textAnchor: 'middle'
			});
		}
		text(svg, PAD.left + plotW / 2, PAD.top + bodyH + 32, 'Nilai kontribusi kanal', 'axis-title', {
			textAnchor: 'middle'
		});

		var y = PAD.top;
		for (var gi = 0; gi < groups.length; gi++) {
			var grp = groups[gi];

			text(svg, 0, y + 13, grp.label, null, {
				fill: 'var(--text-primary)',
				fontSize: '13px',
				fontWeight: '650'
			});
			text(svg, 0, y + 28, grp.n + ' klaim · ' + grp.note, null, {
				fill: 'var(--text-muted)',
				fontSize: '11.5px'
			});

			var barY = y + HEAD;
			for (var si = 0; si < CHANNEL.series.length; si++) {
				var s = CHANNEL.series[si];
				var v = grp.values[si];
				var w = (v / CHANNEL.max) * plotW;

				text(svg, PAD.left - 12, barY + BAR / 2 + 4, s.name.split(' ')[0], null, {
					fill: 'var(--text-secondary)',
					fontSize: '11.5px',
					textAnchor: 'end'
				});

				var bar = el('path', {
					d: barPath(PAD.left, barY, w, BAR, 4),
					fill: s.color,
					class: 'mark'
				}, svg);

				var valLabel = text(svg, PAD.left + w + 8, barY + BAR / 2 + 4, fmt(v, 3), 'value-label', {});

				// hit target: the whole row, wider than the painted mark
				var hit = el('rect', {
					x: PAD.left,
					y: barY - 1,
					width: Math.max(w, 1) + 60,
					height: BAR + 2,
					fill: 'transparent',
					tabindex: '0',
					role: 'img'
				}, svg);
				hit.setAttribute(
					'aria-label',
					grp.label + ', kanal ' + s.name + ': ' + fmt(v, 3) + ' dari ' + fmt(CHANNEL.max, 2)
				);

				var describe = function (evt) {
					var box = svg.getBoundingClientRect();
					var px = evt.clientX ? evt.clientX - box.left : PAD.left + w;
					var py = evt.clientY ? evt.clientY - box.top : barY;
					tip.show(px, py, grp.label + ' — ' + grp.n + ' klaim', CHANNEL.series.map(function (sr, idx) {
						return {
							color: sr.color,
							value: fmt(grp.values[idx], 3),
							label: sr.name
						};
					}));
				};

				hit.addEventListener('pointermove', describe);
				hit.addEventListener('pointerenter', describe);
				hit.addEventListener('focus', describe);
				hit.addEventListener('pointerleave', tip.hide);
				hit.addEventListener('blur', tip.hide);
				bar.setAttribute('tabindex', '-1');
				bar.setAttribute('aria-hidden', 'true');
				valLabel.setAttribute('aria-hidden', 'true');

				barY += BAR + GAP;
			}

			y += HEAD + CHANNEL.series.length * BAR + (CHANNEL.series.length - 1) * GAP + GROUP_GAP;
		}
	}

	/* ---------- chart 2: fraud score per queue, mean over observed range ---------- */

	function renderScore(holder, tip) {
		var W = holder.clientWidth;
		if (!W) return;

		var PAD = { top: 6, right: 104, bottom: 34, left: 148 };
		var BAR = 22;
		var ROW = 62;

		var groups = SCORE.groups;
		var plotW = W - PAD.left - PAD.right;
		var bodyH = groups.length * ROW;
		var H = PAD.top + bodyH + PAD.bottom;

		var svg = el('svg', {
			viewBox: '0 0 ' + W + ' ' + H,
			width: W,
			height: H,
			role: 'img',
			'aria-label':
				'Rata-rata skor fraud per antrean triase beserta rentang skor yang terobservasi. ' +
				'Auto-clear 0,086 (0,04–0,14), Review 0,591 (0,40–0,79), Escalate 0,869 (0,80–0,95). ' +
				'Nilai lengkap tersedia pada tabel di bawah grafik.'
		}, holder);
		svg.setAttribute('class', 'chart-svg');

		var x = function (v) {
			return PAD.left + (v / SCORE.max) * plotW;
		};

		for (var t = 0; t < SCORE.ticks.length; t++) {
			var tv = SCORE.ticks[t];
			var gx = x(tv);
			el('line', {
				x1: gx, y1: PAD.top, x2: gx, y2: PAD.top + bodyH,
				class: tv === 0 ? 'axis-line' : 'grid-line'
			}, svg);
			text(svg, gx, PAD.top + bodyH + 18, fmt(tv, 1), 'axis-text', {
				textAnchor: 'middle'
			});
		}
		text(svg, PAD.left + plotW / 2, PAD.top + bodyH + 32, 'Skor fraud (0–1)', 'axis-title', {
			textAnchor: 'middle'
		});

		for (var gi = 0; gi < groups.length; gi++) {
			var grp = groups[gi];
			var rowY = PAD.top + gi * ROW;
			var barY = rowY + 20;

			text(svg, 0, rowY + 13, grp.label, null, {
				fill: 'var(--text-primary)',
				fontSize: '13px',
				fontWeight: '650'
			});
			text(svg, 0, rowY + 28, grp.n + ' klaim · risiko ' + grp.state, null, {
				fill: 'var(--text-muted)',
				fontSize: '11.5px'
			});

			// observed range as a floating bar
			var rx = x(grp.min);
			var rw = x(grp.max) - rx;
			var range = el('path', {
				d: rangePath(rx, barY, rw, BAR, 4),
				fill: grp.color,
				class: 'mark'
			}, svg);
			range.setAttribute('aria-hidden', 'true');

			// mean marker — a hairline crossing the range bar
			var mx = x(grp.mean);
			el('line', {
				x1: mx, y1: barY - 7, x2: mx, y2: barY + BAR + 7,
				stroke: 'var(--text-primary)',
				strokeWidth: '2',
				'stroke-linecap': 'round'
			}, svg);

			text(svg, mx, barY - 12, 'rata-rata ' + fmt(grp.mean, 3), null, {
				fill: 'var(--text-primary)',
				fontSize: '11px',
				fontWeight: '600',
				textAnchor: 'middle'
			});

			// value + range in the right-hand column
			text(svg, W - PAD.right + 12, barY + BAR / 2 + 4, fmt(grp.mean, 3), 'value-label', {});
			text(svg, W - PAD.right + 12, barY + BAR / 2 + 20, fmt(grp.min, 2) + '–' + fmt(grp.max, 2), null, {
				fill: 'var(--text-muted)',
				fontSize: '10.5px'
			});

			var hit = el('rect', {
				x: PAD.left,
				y: barY - 8,
				width: plotW,
				height: BAR + 16,
				fill: 'transparent',
				tabindex: '0',
				role: 'img'
			}, svg);
			hit.setAttribute(
				'aria-label',
				grp.label + ', rata-rata skor ' + fmt(grp.mean, 3) +
				', rentang ' + fmt(grp.min, 2) + ' sampai ' + fmt(grp.max, 2) +
				', nilai klaim ' + grp.value
			);

			var describe = function (evt) {
				var box = svg.getBoundingClientRect();
				var px = evt.clientX ? evt.clientX - box.left : mx;
				var py = evt.clientY ? evt.clientY - box.top : barY;
				tip.show(px, py, grp.label + ' — ' + grp.n + ' klaim', [
					{ color: grp.color, value: fmt(grp.mean, 3), label: 'rata-rata skor fraud' },
					{ value: fmt(grp.min, 2) + '–' + fmt(grp.max, 2), label: 'rentang terobservasi' },
					{ value: grp.value, label: 'nilai klaim' }
				]);
			};

			hit.addEventListener('pointermove', describe);
			hit.addEventListener('pointerenter', describe);
			hit.addEventListener('focus', describe);
			hit.addEventListener('pointerleave', tip.hide);
			hit.addEventListener('blur', tip.hide);
		}
	}

	/* ---------- mount ---------- */

	function mount() {
		var holders = document.querySelectorAll('.chart-holder[data-chart]');
		if (!holders.length) return;

		Array.prototype.forEach.call(holders, function (holder) {
			holder.textContent = '';
			var tip = new Tooltip(holder);
			var kind = holder.getAttribute('data-chart');

			var draw = function () {
				// clear previous render, keep the tooltip node
				var svgs = holder.querySelectorAll('svg');
				Array.prototype.forEach.call(svgs, function (s) {
					s.remove();
				});
				if (kind === 'channel') {
					renderChannel(holder, tip);
				} else if (kind === 'score') {
					renderScore(holder, tip);
				}
			};

			draw();

			if (window.ResizeObserver) {
				var pending = false;
				var ro = new ResizeObserver(function () {
					if (pending) return;
					pending = true;
					window.requestAnimationFrame(function () {
						pending = false;
						draw();
					});
				});
				ro.observe(holder);
			} else {
				window.addEventListener('resize', draw);
			}
		});
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', mount);
	} else {
		mount();
	}
})();
