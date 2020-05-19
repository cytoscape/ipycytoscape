// Copyright (c) Mariana Meireles
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  WidgetModel,
  WidgetView,
} from '@jupyter-widgets/base';

// eslint-disable-next-line @typescript-eslint/no-var-requires
const widgets = require('@jupyter-widgets/base');

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

import cytoscape from 'cytoscape';
// @ts-ignore
import cola from 'cytoscape-cola';
// @ts-ignore
import popper from 'cytoscape-popper';
// @ts-ignore
import Tippy, { Instance } from 'tippy.js';
// @ts-ignore
import dagre from 'cytoscape-dagre';

import 'tippy.js/themes/material.css';

cytoscape.use(popper);
cytoscape.use(dagre);
cytoscape.use(cola);

export class NodeModel extends WidgetModel {
  defaults() {
    return {
      ...super.defaults(),
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
    };
  }

  static model_name = 'NodeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NodeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class EdgeModel extends WidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: EdgeModel.model_name,
      _model_module: EdgeModel.model_module,
      _model_module_version: EdgeModel.model_module_version,
      // _view_name: EdgeModel.view_name,
      // _view_module: EdgeModel.view_module,
      // _view_module_version: EdgeModel.view_module_version,

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
    };
  }

  static serializers: ISerializers = {
    ...WidgetModel.serializers,
  };

  static model_name = 'EdgeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  // static view_name = 'EdgeView';
  // static view_module = MODULE_NAME;
  // static view_module_version = MODULE_VERSION;
}

export class GraphModel extends WidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: 'GraphModel',
      _model_module: GraphModel.model_module,
      _model_module_version: GraphModel.model_module_version,
      nodes: [],
      edges: [],
    };
  }

  static serializers: ISerializers = {
    nodes: { deserialize: widgets.unpack_models },
    edges: { deserialize: widgets.unpack_models },
    ...WidgetModel.serializers,
  };

  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;

  converts_dict() {
    const graph: Array<any> = [];

    for (let i = 0; i < this.attributes.nodes.length; i++) {
      const node = this.attributes.nodes[i];
      graph.push({
        group: 'nodes',
        data: node.get('data'),
        classes: node.get('classes'),
      });
    }
    for (let j = 0; j < this.attributes.edges.length; j++) {
      const edge = this.attributes.edges[j];
      graph.push({
        group: 'edges',
        data: edge.get('data'),
        classes: edge.get('classes'),
      });
    }

    return graph;
  }
}

export class CytoscapeModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
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
    ...DOMWidgetModel.serializers,
  };

  static model_name = 'CytoscapeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CytoscapeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class NodeView extends WidgetView {
  parentModel: any;

  constructor(params: any) {
    super({
      model: params.model,
      options: params.options,
    });
    this.parentModel = this.options.parentModel;

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

  //TODO: not sure if this is necessary to propagate the changes...
  groupChanged() {
    this.parentModel.set('group', this.model.get('group'));
  }

  removedChanged() {
    this.parentModel.set('removed', this.model.get('removed'));
  }

  selectedChanged() {
    this.parentModel.set('selected', this.model.get('selected'));
  }

  lockedChanged() {
    this.parentModel.set('locked', this.model.get('locked'));
  }

  grabbedChanged() {
    this.parentModel.set('grabbed', this.model.get('grabbed'));
  }

  grabbableChanged() {
    this.parentModel.set('grabbable', this.model.get('grabbable'));
  }

  classesChanged() {
    this.parentModel.set('classes', this.model.get('classes'));
  }

  dataChanged() {
    this.parentModel.set('data', this.model.get('data'));
  }

  positionChanged() {
    this.parentModel.set('position', this.model.get('position'));
  }
}

// export
// class EdgeView extends WidgetView {
//   parentModel: any;

//   constructor(params: any) {
//     super({
//       model: params.model,
//       options: params.options
//     });
//   this.parentModel = this.options.parentModel;

//   this.model.on('change:group', this.groupChanged, this);
//   this.model.on('change:removed', this.removedChanged, this);
//   this.model.on('change:selected', this.selectedChanged, this);
//   this.model.on('change:locked', this.lockedChanged, this);
//   this.model.on('change:grabbed', this.grabbedChanged, this);
//   this.model.on('change:grabbable', this.grabbableChanged, this);
//   this.model.on('change:classes', this.classesChanged, this);
//   this.model.on('change:data', this.dataChanged, this);
//   this.model.on('change:position', this.positionChanged, this);
//   }

//   //TODO: not sure if this is necessary to propagate the changes...
//   groupChanged() {
//     this.parentModel.set("group", this.model.get('group'));
//   }

//   removedChanged() {
//     this.parentModel.set("removed", this.model.get('removed'));
//   }

//   selectedChanged() {
//     this.parentModel.set("selected", this.model.get('selected'));
//   }

//   lockedChanged() {
//     this.parentModel.set("locked", this.model.get('locked'));
//   }

//   grabbedChanged() {
//     this.parentModel.set("grabbed", this.model.get('grabbed'));
//   }

//   grabbableChanged() {
//     this.parentModel.set("grabbable", this.model.get('grabbable'));
//   }

//   classesChanged() {
//     this.parentModel.set("classes", this.model.get('classes'));
//   }

//   dataChanged() {
//     this.parentModel.set("data", this.model.get('data'));
//   }

//   positionChanged() {
//     this.parentModel.set("position", this.model.get('position'));
//   }
// }

export class CytoscapeView extends DOMWidgetView {
  cytoscape_obj: any;
  is_rendered = false;
  nodeViews: any = [];
  edgeViews: any = [];

  render() {
    this.el.classList.add('custom-widget');

    this.nodeViews = new widgets.ViewList(
      this.addNodeModel,
      this.removeNodeView,
      this
    );
    this.nodeViews.update(this.model.get('graph').get('nodes'));

    // this.edgeViews = new widgets.ViewList(this.addEdgeModel, this.removeEdgeView, this);
    // this.edgeViews.update(this.model.get('graph').get('edges'));

    this.value_changed();

    this.model.get('graph').on('change:nodes', this.value_changed, this);
    this.model.get('graph').on('change:edges', this.value_changed, this);
    //TODO: not sure if these are useful, the one for style is not
    //but for layout it seems to make a difference. Need to test and
    //remove the ones that are not and figure out why
    // TODO 2:
    // some of these changes do not require re-running init_render
    // there are cytoscapejs functions that can be called to run change
    // these options
    this.model.on('change:min_zoom', this.value_changed, this);
    this.model.on('change:max_zoom', this.value_changed, this);
    this.model.on('change:zooming_enabled', this.value_changed, this);
    this.model.on('change:user_zooming_enabled', this.value_changed, this);
    this.model.on('change:panning_enabled', this.value_changed, this);
    this.model.on('change:box_selection_enabled', this.value_changed, this);
    this.model.on('change:selection_type', this.value_changed, this);
    this.model.on('change:touch_tap_threshold', this.value_changed, this);
    this.model.on('change:desktop_tap_threshold', this.value_changed, this);
    this.model.on('change:autolock', this.value_changed, this);
    this.model.on('change:auto_ungrabify', this.value_changed, this);
    this.model.on('change:auto_unselectify', this.value_changed, this);
    this.model.on('change:cytoscape_layout', this.value_changed, this);
    this.model.on('change:cytoscape_style', this.value_changed, this);
    this.model.on('change:elements', this.value_changed, this);

    this.displayed.then(() => {
      this.init_render();
    });
  }

  value_changed() {
    if (this.is_rendered) {
      console.log('value_changed');
      this.init_render();
    }
  }

  init_render() {
    if (this.model.get('graph') !== null) {
      this.is_rendered = true;
      this.cytoscape_obj = cytoscape({
        container: this.el,
        minZoom: this.model.get('min_zoom'),
        maxZoom: this.model.get('max_zoom'),
        zoomingEnabled: this.model.get('zooming_enabled'),
        userZoomingEnabled: this.model.get('user_zooming_enabled'),
        panningEnabled: this.model.get('panning_enabled'),
        boxSelectionEnabled: this.model.get('box_selection_enabled'),
        selectionType: this.model.get('selection_type'),
        touchTapThreshold: this.model.get('touch_tap_threshold'),
        desktopTapThreshold: this.model.get('desktop_tap_threshold'),
        autolock: this.model.get('autolock'),
        autoungrabify: this.model.get('auto_ungrabify'),
        autounselectify: this.model.get('auto_unselectify'),
        headless: this.model.get('headless'),
        styleEnabled: this.model.get('style_enabled'),
        hideEdgesOnViewport: this.model.get('hide_edges_on_viewport'),
        textureOnViewport: this.model.get('texture_on_viewport'),
        motionBlur: this.model.get('motion_blur'),
        motionBlurOpacity: this.model.get('motion_blur_opacity'),
        wheelSensitivity: this.model.get('wheel_sensitivity'),
        layout: this.model.get('cytoscape_layout'),
        style: this.model.get('cytoscape_style'),
        elements: this.model.get('graph').converts_dict(),
      });

      this.cytoscape_obj.on('click', 'node', (e: any) => {
        const node = e.target;
        const ref = node.popperRef();
        const dummyDomEle = document.createElement('div');

        if (node.data().name) {
          const tip = Tippy(dummyDomEle, {
            //TODO: add a pretty tippy
            trigger: 'manual',
            lazy: false,
            arrow: true,
            theme: 'material',
            placement: 'bottom',
            content: () => {
              /*
                  TODO:
                  Currently this function is mapping to one attribute inside
                  nodes[data], which in this case is name.
                  The backend is using that to import various datas from
                  DataFrames, the problem is that data will appear unformatted.
                  Not even line breaks are working for some reason.
                  Make the visualization better, see issue: #33
                */
              const content = document.createElement('div');
              content.innerHTML = node.data().name;
              return content;
            },
            onCreate: (instance: Instance | undefined) => {
              if (instance && instance.popperInstance) {
                instance.popperInstance.reference = ref;
              }
            },
          });
          tip.show();
        }
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

  // addEdgeModel(EdgeModel: any) {
  //   console.log('adding edge model')
  //     return this.create_child_view(EdgeModel, {
  //         cytoscapeView: this,
  //         parentModel: this.model,
  //     });
  // }

  // removeEdgeView(edgeView: any) {
  //     edgeView.remove();
  // }
}
