// Copyright (c) 2020, QuantStack and ipycytoscape Contributors
//
// Distributed under the terms of the Modified BSD License.
//
// The full license is in the file LICENSE, distributed with this software.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  Dict,
} from '@jupyter-widgets/base';

// eslint-disable-next-line @typescript-eslint/no-var-requires
const widgets = require('@jupyter-widgets/base');

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

import cytoscape, { Core } from 'cytoscape';
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

// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { NodeModel, EdgeModel } from './graph';

cytoscape.use(popper);
cytoscape.use(dagre);
cytoscape.use(klay);
cytoscape.use(cola);

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

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('msg:custom', this.processMessage.bind(this));
  }

  static serializers: ISerializers = {
    graph: { deserialize: widgets.unpack_models },
    ...DOMWidgetModel.serializers,
  };

  private processMessage(command: any, buffers: any) {
    if (command.name === 'layout') {
      this.forEachView((view) => {
        view.cytoscape_obj.layout(this.get('cytoscape_layout')).run();
      });
    }
  }

  private forEachView(callback: (view: CytoscapeView) => void) {
    for (const view_id in this.views) {
      this.views[view_id].then((view: CytoscapeView) => {
        callback(view);
      });
    }
  }

  static model_name = 'CytoscapeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'CytoscapeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
  views: Dict<Promise<CytoscapeView>>;
}

export class CytoscapeView extends DOMWidgetView {
  cytoscape_obj: Core;
  is_rendered = false;
  nodeViews: any = [];
  edgeViews: any = [];
  monitored: any = {};

  render() {
    this.el.classList.add('custom-widget');

    this.displayed.then(() => {
      this.init_render();
      this.cytoscape_obj.startBatch();
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
      this.cytoscape_obj.endBatch();
      this.cytoscape_obj
        .elements()
        .layout(this.model.get('cytoscape_layout'))
        .run();
    });

    this.model
      .get('graph')
      .on_some_change(['nodes', 'edges'], this._updateViewLists, this);

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
  }

  value_changed() {
    if (this.is_rendered) {
      // Rerendering creates a new cytoscape object, so we will need to re-add
      // interaction handlers. Set `monitored` to empty to trigger this.
      this.monitored = {};
      this.init_render();
    }
  }

  private _updateViewLists() {
    this.nodeViews.update(this.model.get('graph').get('nodes'));
    this.edgeViews.update(this.model.get('graph').get('edges'));
    this.cytoscape_obj
      .elements()
      .layout(this.model.get('cytoscape_layout'))
      .run();
    console.log('whole cytoscape relayout');
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
        style: this.model.get('cytoscape_style'),
        elements: [],
      });

      // we need to set listeners at initial render in case interaction was
      // added before the graph was displayed.
      // const monitored = this.model.get('monitored');
      this.listenForUserEvents();

      this.cytoscape_obj.on('click', (e: any) => {
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
    this.cytoscape_obj.userPanningEnabled(
      this.model.get('user_panning_enabled')
    );
  }
  private _updateBoxSelectionEnabled() {
    this.cytoscape_obj.boxSelectionEnabled(
      this.model.get('box_selection_enabled')
    );
  }
  private _updateSelectionType() {
    // I think that @types may have gotten this wrong?
    (this.cytoscape_obj as any).selectionType(this.model.get('selection_type'));
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
    this.cytoscape_obj.layout(this.model.get('cytoscape_layout')).run();
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

  /**
   * Add the listeners for traits that are common to nodes and edges
   */
  _addElementListeners(
    ele: cytoscape.CollectionReturnValue,
    view: DOMWidgetView
  ) {
    ele.on('select', (event) => {
      view.model.set('selected', true);
      view.model.save_changes();
    });
    ele.on('unselect', (event) => {
      view.model.set('selected', false);
      view.model.save_changes();
    });
    ele.on('remove', (event) => {
      view.model.set('removed', true);
      view.model.save_changes();
    });
  }

  async addNodeModel(NodeModel: NodeModel) {
    const node = this.cytoscape_obj.add(NodeModel.asCyObj());
    const child = await this.create_child_view(NodeModel, {
      cytoscapeView: this,
    });
    this._addElementListeners(node, child);
    node.on('grab', (event) => {
      child.model.set('grabbed', true);
      child.model.save_changes();
    });
    node.on('free', (event) => {
      child.model.set('grabbed', false);
      child.model.save_changes();
    });
    return child;
  }

  removeNodeView(nodeView: any) {
    nodeView.remove();
  }

  async addEdgeModel(EdgeModel: EdgeModel) {
    const edge = this.cytoscape_obj.add(EdgeModel.asCyObj());
    const child = await this.create_child_view(EdgeModel, {
      cytoscapeView: this,
    });
    this._addElementListeners(edge, child);
    return child;
  }

  removeEdgeView(edgeView: any) {
    edgeView.remove();
  }
}
