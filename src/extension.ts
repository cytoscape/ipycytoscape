// Copyright (c) 2020, QuantStack, Mariana Meireles and ipycytoscape Contributors
//
// Distributed under the terms of the Modified BSD License.
//
// The full license is in the file LICENSE, distributed with this software.

(window as any).__webpack_public_path__ =
  document.querySelector('body')!.getAttribute('data-base-url') + // eslint-disable-line @typescript-eslint/no-non-null-assertion
  'nbextensions/jupyter-cytoscape';

export * from './index';
