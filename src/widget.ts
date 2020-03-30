// Copyright (c) Mariana Meireles
// Distributed under the terms of the Modified BSD License.

// import * as widgets from '@jupyter-widgets/base';

import {
  DOMWidgetModel, DOMWidgetView, ISerializers, WidgetModel, WidgetView
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
      _model_name: NodeModel.model_name,
      _model_module: NodeModel.model_module,
      _model_module_version: NodeModel.model_module_version,
      _view_name: NodeModel.view_name,
      _view_module: NodeModel.view_module,
      _view_module_version: NodeModel.view_module_version,

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

  static model_name = 'NodeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NodeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
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
      let graph: {nodes:Array<object>, edges:Array<object>} = {nodes: [], edges: []};

      var node: object;
      for (var i: number = 0; i < this.attributes.nodes.length; i++) {
        node = this.attributes.nodes[i].get('data')
        graph.nodes.push(node);
      }
      //TODO: adding edges is not working
      //Error setting state: An element must be of type `nodes` or `edges`; you specified `coexp`
      var edge: object;
      for (var j: number = 0; j < this.attributes.edges.length; j++) {
        console.log('🌈')
        console.log(this.attributes.edges[j])
        console.log(this.attributes.edges[j].get('data'))
        edge = this.attributes.edges[j].get('data')
        graph.edges.push(edge);
      }
      return graph;
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

      auto_unselectify: true,
      box_selection_enabled: false,
      cytoscape_layout: {},
      cytoscape_style: [],
      elements: [],
      zoom: 0,
      rendered_position: {},

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
class NodeView extends WidgetView {
    parentModel: any;
    constructor(params: any) {
        console.log('🦋')
        console.log(params);
        // console.log(parentModel);
        super({
          model: params.model,
          options: params.options
        }); 
        console.log(arguments);  
        this.parentModel = this.options.parentModel;
        console.log(this.model);
        this.model.on('change:group', this.groupChanged, this);
        this.model.on('change:removed', this.removedChanged, this);
        this.model.on('change:selected', this.selectedChanged, this);
        this.model.on('change:locked', this.lockedChanged, this);
        this.model.on('change:grabbed', this.grabbedChanged, this);
        this.model.on('change:grabbable', this.grabbableChanged, this);
        this.model.on('change:classes', this.classesChanged, this);
        this.model.on('change:data', this.dataChanged, this);
        this.model.on('change:position', this.positionChanged, this);
    }

    groupChanged() {
      this.parentModel.set("group", this.model.get('group'));
    }

    removedChanged() {
      this.parentModel.set("removed", this.model.get('removed'));
    }

    selectedChanged() {
      this.parentModel.set("selected", this.model.get('selected'));
    }

    lockedChanged() {
      this.parentModel.set("locked", this.model.get('locked'));
    }

    grabbedChanged() {
      this.parentModel.set("grabbed", this.model.get('grabbed'));
    }

    grabbableChanged() {
      this.parentModel.set("grabbable", this.model.get('grabbable'));
    }

    classesChanged() {
      this.parentModel.set("classes", this.model.get('classes'));
    }

    dataChanged() {
      this.parentModel.set("data", this.model.get('data'));
    }

    positionChanged() {
      this.parentModel.set("position", this.model.get('position'));
    }
}

export
class CytoscapeView extends DOMWidgetView {
  cytoscape_obj: any;
  is_rendered: boolean = false;
  nodeViews: any = [];

/*TODO:
[x] - create a way to observe individually change on nodes
[] - show tippys on click
[] - add zoom_change
[] - add rendered_position_change
[x] - add support for edges
*/

  render() {
    this.el.classList.add('custom-widget');

    this.nodeViews = new widgets.ViewList(this.addNodeModel, this.removeNodeView, this);
    this.nodeViews.update(this.model.get('graph').get('nodes'));
    // this.listenTo(this.model, 'change:nodes', this.handleNodesChange);

    this.value_changed();
    this.model.get('graph').on('change:nodes', this.value_changed, this);
    this.model.get('graph').on('change:edges', this.value_changed, this);
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
    if (this.model.get('graph') != null) {
        this.is_rendered = true;
        this.cytoscape_obj = cytoscape({
          container: this.el,
          elements: this.model.get('graph').converts_dict(),
        });
    }
  }

  addNodeModel(NodeModel: any) {
      return this.create_child_view(NodeModel, {
          cytoscapeView: this,
          parentModel: this.model,
      });
  }

  removeNodeView(nodeView: any) {
      nodeView.remove();
  }

  // handleNodesChange() {
  //     this.nodeViews.update(this.model.get('nodes'));
  //     // If top level nodes are changed, icons disappear
  //     // So reload them for all visible nodes
  //     Promise.all(this.nodeViews.views).then(function(views) {
  //       for(var view in views){
  //         views[view].setOpenCloseIcon(true);
  //       }
  //     });
  // }


}
