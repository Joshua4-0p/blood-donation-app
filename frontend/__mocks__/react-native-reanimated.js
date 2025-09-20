module.exports = {
  addListener: jest.fn(),
  removeListener: jest.fn(),
  createAnimatedComponent: (component) => component,
  Value: class {},
  event: () => jest.fn(),
  config: () => jest.fn(),
  Easing: {
    linear: jest.fn(),
    ease: jest.fn(),
  },
};
