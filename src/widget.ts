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

// @ts-ignore
import klay from 'cytoscape-klay';

import 'tippy.js/themes/material.css';

cytoscape.use(popper);
cytoscape.use(dagre);
cytoscape.use(klay);
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
      _view_name: EdgeModel.view_name,
      _view_module: EdgeModel.view_module,
      _view_module_version: EdgeModel.view_module_version,

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

  static model_name = 'EdgeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'EdgeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
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
        selected: node.get('selected'),
        selectable: node.get('selectable'),
        locked: node.get('locked'),
        grabbed: node.get('grabbed'),
        classes: node.get('classes'),
        position: node.get('position'),
      });
    }
    for (let j = 0; j < this.attributes.edges.length; j++) {
      const edge = this.attributes.edges[j];
      graph.push({
        group: 'edges',
        data: edge.get('data'),
        selected: edge.get('selected'),
        selectable: edge.get('selectable'),
        locked: edge.get('locked'),
        grabbed: edge.get('grabbed'),
        classes: edge.get('classes'),
        position: edge.get('position'),
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
      tooltip_source: '',

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
  cytoscapeView: any;
  private cyId: string;

  constructor(params: any) {
    super({
      model: params.model,
      options: params.options,
    });
    this.cytoscapeView = this.options.cytoscapeView;

    this.model.on('change:group', this.valueChanged, this);
    this.model.on('change:removed', this.valueChanged, this);
    this.model.on('change:selected', this.valueChanged, this);
    this.model.on('change:locked', this.valueChanged, this);
    this.model.on('change:grabbed', this.valueChanged, this);
    this.model.on('change:grabbable', this.valueChanged, this);
    this.model.on('change:classes', this._updateClasses, this);
    this.model.on('change:data', this.valueChanged, this);
    this.model.on('change:position', this.valueChanged, this);
    this.cyId = this.model.get('data')['id'];
  }

  private _updateClasses() {
    const elem = this.cytoscapeView.cytoscape_obj.getElementById(this.cyId);
    elem.classes(this.model.get('classes'));
  }

  valueChanged() {
    this.cytoscapeView.value_changed();
  }
}

export class EdgeView extends WidgetView {
  cytoscapeView: any;
  private cyId: string;

  constructor(params: any) {
    super({
      model: params.model,
      options: params.options,
    });
    this.cytoscapeView = this.options.cytoscapeView;

    this.model.on('change:group', this.valueChanged, this);
    this.model.on('change:removed', this.valueChanged, this);
    this.model.on('change:selected', this.valueChanged, this);
    this.model.on('change:locked', this.valueChanged, this);
    this.model.on('change:grabbed', this.valueChanged, this);
    this.model.on('change:grabbable', this.valueChanged, this);
    this.model.on('change:classes', this._updateClasses, this);
    this.model.on('change:data', this.valueChanged, this);
    this.model.on('change:position', this.valueChanged, this);
    this.cyId = this.model.get('data')['id'];
  }
  private _updateClasses() {
    const elem = this.cytoscapeView.cytoscape_obj.getElementById(this.cyId);
    elem.classes(this.model.get('classes'));
  }

  valueChanged() {
    this.cytoscapeView.value_changed();
  }
}

export class CytoscapeView extends DOMWidgetView {
  cytoscape_obj: any;
  is_rendered = false;
  nodeViews: any = [];
  edgeViews: any = [];
  monitored: any = {};

  render() {
    this.el.classList.add('custom-widget');

    this.nodeViews = new widgets.ViewList(
      this.addNodeModel,
      this.removeNodeView,
      this
    );
    this.nodeViews.update(this.model.get('graph').get('nodes'));

    this.edgeViews = new widgets.ViewList(
      this.addEdgeModel,
      this.removeEdgeView,
      this
    );
    this.edgeViews.update(this.model.get('graph').get('edges'));

    this.value_changed();

    this.model.get('graph').on('change:nodes', this.value_changed, this);
    this.model.get('graph').on('change:edges', this.value_changed, this);

    //Python attributes that must be sync. with frontend
    this.model.on('change:min_zoom', this._updateMinZoom, this);
    this.model.on('change:max_zoom', this._updateMaxZoom, this);
    this.model.on('change:zooming_enabled', this._updateZoomingEnabled, this);
    this.model.on(
      'change:user_zooming_enabled',
      this._updateUserZoomingEnabled,
      this
    );
    this.model.on('change:panning_enabled', this._updatePanningEnabled, this);
    this.model.on(
      'change:user_panning_enabled',
      this._updateUserPanningEnabled,
      this
    );
    this.model.on(
      'change:box_selection_enabled',
      this._updateBoxSelectionEnabled,
      this
    );
    this.model.on('change:selection_type', this._updateSelectionType, this);
    this.model.on('change:touch_tap_threshold', this.value_changed, this);
    this.model.on('change:desktop_tap_threshold', this.value_changed, this);
    this.model.on('change:autolock', this._updateAutolock, this);
    this.model.on('change:auto_ungrabify', this._updateAutoUngrabify, this);
    this.model.on('change:auto_unselectify', this._updateAutoUnselectify, this);
    this.model.on('change:cytoscape_layout', this._updateLayout, this);
    this.model.on('change:cytoscape_style', this._updateStyle, this);
    this.model.on('change:elements', this.value_changed, this);
    this.model.on('change:pixel_ratio', this.value_changed, this);
    this.model.on(
      'change:_interaction_handlers',
      this.listenForUserEvents,
      this
    );

    const layout = this.model.get('layout');
    if (layout !== null) {
      layout.on_some_change(['width', 'height'], this._resize, this);
    }

    this.displayed.then(() => {
      this.init_render();
    });
  }

  value_changed() {
    if (this.is_rendered) {
      // Rerendering creates a new cytoscape object, so we will need to re-add
      // interaction handlers. Set `monitored` to empty to trigger this.
      this.monitored = {};
      this.init_render();
    }
  }

  listenForUserEvents() {
    const new_monitored = this.model.get('_interaction_handlers');
    // If the plot hasn't been displayed yet, we can't add handlers yet. By
    // returning immediately, we avoid marking them as set, so we'll end up
    // setting them when the graph is finally displayed.
    if (!this.cytoscape_obj) {
      return;
    }
    for (const widgtype in new_monitored) {
      if (Object.prototype.hasOwnProperty.call(new_monitored, widgtype)) {
        for (let i = 0; i < new_monitored[widgtype].length; i++) {
          const evnttype = new_monitored[widgtype][i];
          if (this.monitored[widgtype]) {
            if (this.monitored[widgtype].includes(evnttype)) {
              return;
            } else {
              this.monitored[widgtype].push(evnttype);
            }
          } else {
            this.monitored[widgtype] = [evnttype];
          }
          this.cytoscape_obj.on(evnttype, widgtype, (e: any) => {
            this.send({
              event: evnttype,
              widget: widgtype,
              data: e.target.json(),
            });
          });
        }
      }
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
        pixelRatio: this.model.get('pixel_ratio'),
        layout: this.model.get('cytoscape_layout'),
        style: this.model.get('cytoscape_style'),
        elements: this.model.get('graph').converts_dict(),
      });

      // we need to set listeners at initial render in case interaction was
      // added before the graph was displayed.
      // const monitored = this.model.get('monitored');
      this.listenForUserEvents();

      this.cytoscape_obj.on('click', 'node', (e: any) => {
        const node = e.target;
        const ref = node.popperRef();
        const dummyDomEle = document.createElement('div');

        const tooltip_source = this.model.get('tooltip_source');
        if (node.data()[tooltip_source]) {
          const tip = Tippy(dummyDomEle, {
            //TODO: add a pretty tippy
            trigger: 'manual',
            lazy: false,
            arrow: true,
            theme: 'material',
            placement: 'bottom',
            content: () => {
              const content = document.createElement('div');
              content.innerHTML = node
                .data()
                [tooltip_source].replace(/(?:\r\n|\r|\n)/g, '<br>');
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
  private _updateMinZoom() {
    this.cytoscape_obj.minZoom(this.model.get('min_zoom'));
  }
  private _updateMaxZoom() {
    this.cytoscape_obj.maxZoom(this.model.get('max_zoom'));
  }
  private _updateZoomingEnabled() {
    this.cytoscape_obj.zoomingEnabled(this.model.get('zooming_enabled'));
  }
  private _updateUserZoomingEnabled() {
    this.cytoscape_obj.userZoomingEnabled(
      this.model.get('user_zooming_enabled')
    );
  }
  private _updatePanningEnabled() {
    this.cytoscape_obj.panningEnabled(this.model.get('panning_enabled'));
  }
  private _updateUserPanningEnabled() {
    this.cytoscape_obj.UserPanningEnabled(
      this.model.get('user_panning_enabled')
    );
  }
  private _updateBoxSelectionEnabled() {
    this.cytoscape_obj.boxSelectionEnabled(
      this.model.get('box_selection_enabled')
    );
  }
  private _updateSelectionType() {
    this.cytoscape_obj.selectionType(this.model.get('selection_type'));
  }
  private _updateAutolock() {
    this.cytoscape_obj.autolock(this.model.get('autolock'));
  }
  private _updateAutoUngrabify() {
    this.cytoscape_obj.autoungrabify(this.model.get('auto_ungrabify'));
  }
  private _updateAutoUnselectify() {
    this.cytoscape_obj.autounselectify(this.model.get('auto_unselectify'));
  }
  private _updateLayout() {
    this.cytoscape_obj.layout(this.model.get('layout'));
  }
  private _updateStyle() {
    this.cytoscape_obj.style(this.model.get('cytoscape_style'));
  }

  private _resize() {
    if (this.cytoscape_obj) {
      this.cytoscape_obj.resize();
      this.cytoscape_obj.fit();
    }
  }

  addNodeModel(NodeModel: any) {
    return this.create_child_view(NodeModel, {
      cytoscapeView: this,
    });
  }

  removeNodeView(nodeView: any) {
    nodeView.remove();
  }

  addEdgeModel(EdgeModel: any) {
    return this.create_child_view(EdgeModel, {
      cytoscapeView: this,
    });
  }

  removeEdgeView(edgeView: any) {
    edgeView.remove();
  }
}
