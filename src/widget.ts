// Copyright (c) Mariana Meireles
// Distributed under the terms of the Modified BSD License.

// import * as widgets from '@jupyter-widgets/base';

import {
  DOMWidgetModel, DOMWidgetView, ISerializers, WidgetModel
} from '@jupyter-widgets/base';

var widgets = require('@jupyter-widgets/base');

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
class EdgeModel extends WidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: 'EdgeModel',
      _model_module: EdgeModel.model_module,
      _model_module_version: EdgeModel.model_module_version,
      id: 0,
    }
  };

  static serializers: ISerializers = {
      ...WidgetModel.serializers
    }

  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export
class NodeModel extends WidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: 'NodeModel',
      _model_module: NodeModel.model_module,
      _model_module_version: NodeModel.model_module_version,
      id: 0,
      idInt: 0,
      name: '',
      score: 0,
      query: false,
      gene: false,
      label: '',
      x: 0,
      y: 0,
      group: '',
      removed: false,
      selected: false,
      selectable: false,
      locked: false,
      grabbed: false,
      grabbable: false,
      classes: '',
      data: {},
      position: {},
    }
  };

//I don't think this one needs a serializer
  static serializers: ISerializers = {
      ...WidgetModel.serializers
    }

  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export
class GraphModel extends WidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: 'GraphModel',
      _model_module: GraphModel.model_module,
      _model_module_version: GraphModel.model_module_version,
      nodes: [],
      edges: [],
    }
  };

  static serializers: ISerializers = {
      nodes: { deserialize: widgets.unpack_models },
      edges: { deserialize: widgets.unpack_models },
      ...WidgetModel.serializers
    }

  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;

  converts_dict() {
    console.log('☁️');
    let node_list: Array<object> = [{'nodes': '', 'edges': ''}];
      // let data: object;
      // let position: object = {}
      let node: object = {}
      for (var i: number = 0; i < this.attributes.nodes.length; i++) {
        node = this.attributes.nodes[i].attributes.data
        // position = this.attributes.nodes[i].attributes.data.position
        // node = {'data': data, 'position': position}
        // console.log(data)
        console.log(node_list)
        node_list.push(node)
      }
      return node_list;
  }
}


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
      graph: null,
    };
  }

  static serializers: ISerializers = {
      graph: { deserialize: widgets.unpack_models },
      ...DOMWidgetModel.serializers
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
    this.model.get('graph').on('change:nodes', this.value_changed, this);
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
    console.log('🦋')
    if (this.model.get('graph') != null) {
        this.is_rendered = true;
        this.cytoscape_obj = cytoscape({
          container: this.el,
          elements: this.model.get('graph').converts_dict(),
        });
    }
    console.log('🦇');
  }

}
