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
// @ts-ignore
import popper from 'cytoscape-popper';
// @ts-ignore
import Tippy from 'tippy.js';
// @ts-ignore
import dagre from 'cytoscape-dagre';

import 'tippy.js/themes/material.css';

cytoscape.use( popper );
cytoscape.use( dagre );
cytoscape.use( cola );

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
      graph: {},
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
    }

  static model_name = 'CytoscapeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CytoscapeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export
class CytoscapeView extends DOMWidgetView {
  cytoscape_obj: any;
  is_rendered: boolean = false;

  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:graph', this.value_changed, this);

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
    this.cytoscape_obj = cytoscape({
      container: this.el,
      elements: this.model.get('graph'),
    });
    console.log(this.cytoscape_obj.graph) //Will print undefined
  }

}
