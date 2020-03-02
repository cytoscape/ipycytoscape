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
      auto_unselectify: true,
      box_selection_enabled: false,
      cytoscape_layout: {},
      cytoscape_style: [],
      elements: [],
      zoom: 0,
      rendered_position: {},
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
  cytoscape_obj: any;
  is_rendered: boolean = false;

  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:auto_unselectify', this.value_changed, this);
    this.model.on('change:box_selection_enabled', this.value_changed, this);
    this.model.on('change:cytoscape_layout', this.value_changed, this);
    this.model.on('change:cytoscape_style', this.value_changed, this);
    this.model.on('change:elements', this.value_changed, this);
    this.model.on('change:zoom', this.zoom_change, this);
    this.model.on('change:rendered_position', this.rendered_position_change, this);

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
      autounselectify: this.model.get('auto_unselectify'),
      boxSelectionEnabled: this.model.get('box_selection_enabled'),
      layout: this.model.get('cytoscape_layout'),
      style: this.model.get('cytoscape_style'),
      elements: this.model.get('elements'),
  });

  this.cytoscape_obj.on('click', 'node', (e: any) => {
    let node = e.target;
    let ref = node.popperRef();
    let dummyDomEle = document.createElement('div');

    if (node.data().name){
      let tip = Tippy(dummyDomEle, {
        //TODO: add a pretty tippy
        trigger: 'manual',
        lazy: false,
        arrow: true,
        theme: 'material',
        placement: 'bottom',
        content: () => {
          //TODO: modularize this, add a function to edit this somehow
          let content = document.createElement('div');
          content.innerHTML = node.data().name;
          return content;
        },
        onCreate: instance => { instance!.popperInstance!.reference = ref; }
      });
      tip.show();
    }
  });

  this.cytoscape_obj.on('zoom', () => {
    this.model.set('zoom', {'level': this.cytoscape_obj.zoom()});
    this.model.save_changes();
  });

  this.cytoscape_obj.on('rendered_position', () => {
    this.model.set('rendered_position', {'renderedPosition': this.cytoscape_obj.rendered_position()});
    this.model.save_changes();
  })
  }

  zoom_change() {
    this.cytoscape_obj.zoom(this.model.get('zoom'));
  }

  rendered_position_change() {
    this.cytoscape_obj.rendered_position(this.model.get('rendered_position'));
  }

}
