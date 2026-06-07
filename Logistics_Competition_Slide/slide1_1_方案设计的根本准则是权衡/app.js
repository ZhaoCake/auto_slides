import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.esm.js';
import RevealHighlight from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.esm.js';
import RevealNotes from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.esm.js';
import RevealSearch from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/search/search.esm.js';
import RevealZoom from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/zoom/zoom.esm.js';
import RevealMarkdown from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/markdown/markdown.esm.js';

Reveal.initialize({
  width: 1600,
  height: 900,
  margin: 0.04,
  minScale: 0.2,
  maxScale: 1.6,
  hash: true,
  slideNumber: 'c/t',
  progress: true,
  controls: true,
  center: false,
  transition: 'slide',
  transitionSpeed: 'default',
  backgroundTransition: 'fade',
  mouseWheel: true,
  touch: true,
  history: true,
  overview: true,
  navigationMode: 'default',
  autoAnimate: true,
  autoAnimateEasing: 'ease-out',
  autoAnimateDuration: 0.6,
  plugins: [
    RevealHighlight,
    RevealNotes,
    RevealSearch,
    RevealZoom,
    RevealMarkdown,
  ],
  markdown: {
    notesSeparator: '^\\s*notes?:',
    smartypants: false,
  },
  highlight: {
    highlightOnLoad: true,
  },
});

Reveal.on('ready', () => {
  document.body.classList.add('deck-ready');
});

Reveal.on('slidechanged', () => {
  document.body.classList.add('slide-active');
  window.setTimeout(() => {
    document.body.classList.remove('slide-active');
  }, 320);
});
