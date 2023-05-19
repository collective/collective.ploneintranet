import { Tooltips } from '@rohberg/volto-slate-glossary/components';

const applyConfig = (config) => {
  config.settings.appExtras = [
    ...config.settings.appExtras,
    {
      match: '/news',
      component: Tooltips,
    },
  ];
  return config;
};

export default applyConfig;
