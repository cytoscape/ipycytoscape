// Copyright (c) Mariana Meireles
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'

import cytoscape from 'cytoscape';
// @ts-ignore
import cola from 'cytoscape-cola';
// import euler from 'cytoscape-euler';

cytoscape.use( cola );
// cytoscape.use( euler );

export
class CytoscapeModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: CytoscapeModel.model_name,
      _model_module: CytoscapeModel.model_module,
      _model_module_version: CytoscapeModel.model_module_version,
      _view_name: CytoscapeModel.view_name,
      _view_module: CytoscapeModel.view_module,
      _view_module_version: CytoscapeModel.view_module_version,
      value : {},
      autounselectify: true,
      boxSelectionEnabled: false,
      cytoscape_layout: {},
      cytoscape_style: [],
      elements: [],
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
    }

  static model_name = 'CytoscapeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CytoscapeView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export
class CytoscapeView extends DOMWidgetView {
  cytoscapemodel: any;
  is_rendered: boolean = false;

  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:autounselectify', this.value_changed, this);
    this.model.on('change:boxSelectionEnabled', this.value_changed, this);
    this.model.on('change:cytoscape_layout', this.value_changed, this);
    this.model.on('change:cytoscape_style', this.value_changed, this);
    this.model.on('change:elements', this.value_changed, this);
    this.displayed.then(() => {
      this.init_render();
    });
  }

  value_changed() {
    if (this.is_rendered) {
        this.init_render();
    }
  }

  init_render() {
    this.is_rendered = true;
    console.log(this.model.get('elements'));
    this.cytoscapemodel = cytoscape({
      container: this.el,
      autounselectify: this.model.get('autounselectify'),
      boxSelectionEnabled: this.model.get('boxSelectionEnabled'),
      layout: this.model.get('cytoscape_layout'),
      style: this.model.get('cytoscape_style'),
      elements: this.model.get('elements'),
    });
  }
}
