const deck = new Reveal({
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
});

deck.initialize();

deck.on('ready', () => {
  document.body.classList.add('deck-ready');
});

deck.on('slidechanged', () => {
  document.body.classList.add('slide-active');
  window.setTimeout(() => {
    document.body.classList.remove('slide-active');
  }, 320);
});
