import { ISerializers, WidgetModel, WidgetView } from '@jupyter-widgets/base';

// eslint-disable-next-line @typescript-eslint/no-var-requires
const widgets = require('@jupyter-widgets/base');

import { MODULE_NAME, MODULE_VERSION } from './version';

import { EdgeSingular, NodeSingular } from 'cytoscape';
import { CytoscapeView } from './widget';

export class ElementModel extends WidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      group: '',
      removed: false,
      selected: false,
      selectable: false,
      locked: false,
      classes: '',
      data: {},
    };
  }
}

export class NodeModel extends ElementModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: NodeModel.model_name,
      _model_module: NodeModel.model_module,
      _model_module_version: NodeModel.model_module_version,
      _view_name: NodeModel.view_name,
      _view_module: NodeModel.view_module,
      _view_module_version: NodeModel.view_module_version,

      position: {},
      grabbed: false,
      grabbable: false,
    };
  }

  static model_name = 'NodeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NodeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class EdgeModel extends ElementModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: EdgeModel.model_name,
      _model_module: EdgeModel.model_module,
      _model_module_version: EdgeModel.model_module_version,
      _view_name: EdgeModel.view_name,
      _view_module: EdgeModel.view_module,
      _view_module_version: EdgeModel.view_module_version,
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

export class ElementView extends WidgetView {
  cytoscapeView: CytoscapeView;
  protected elem: NodeSingular | EdgeSingular;

  constructor(params: any) {
    super({
      model: params.model,
      options: params.options,
    });
    this.cytoscapeView = this.options.cytoscapeView;
    const cyId = this.model.get('data')['id'];
    this.elem = this.cytoscapeView.cytoscape_obj.getElementById(cyId);

    this.model.on('change:group', this.valueChanged, this);
    this.model.on('change:removed', this.valueChanged, this);
    this.model.on('change:selected', this.valueChanged, this);
    this.model.on('change:locked', this.valueChanged, this);
    this.model.on('change:classes', this._updateClasses, this);
    this.model.on('change:data', this._updateData, this);
    this.model.on('change:position', this.valueChanged, this);
  }

  private _updateData() {
    this.elem.data(this.model.get('data'));
  }

  private _updateClasses() {
    this.elem.classes(this.model.get('classes'));
  }

  valueChanged() {
    this.cytoscapeView.value_changed();
  }
}
export class NodeView extends ElementView {
  constructor(params: any) {
    console.log('node constructor');
    super({
      model: params.model,
      options: params.options,
    });
    this.model.on('change:grabbed', () => {
      (this.elem as NodeSingular).grabbed();
    });
    // this.model.on('change:grabbable', () => {
    //   // this casting may be due to an issue with @types/cytoscapejs
    //   // or it may be due to an issue with my understanding of typescript
    //   (this.elem as NodeSingular).grabbable(this.model.get('grabbable'));
    // });
    this.model.on('change:grabbed', this.valueChanged, this);
    this.model.on('change:grabbable', this.valueChanged, this);
  }
}

export class EdgeView extends WidgetView {
  cytoscapeView: CytoscapeView;
  private elem: EdgeSingular;

  constructor(params: any) {
    super({
      model: params.model,
      options: params.options,
    });
    this.cytoscapeView = this.options.cytoscapeView;

    this.model.on('change:group', this.valueChanged, this);
    this.model.on('change:removed', this.valueChanged, this);
    this.model.on('change:selected', this.valueChanged, this);
    this.model.on('change:classes', this._updateClasses, this);
    this.model.on('change:data', this.valueChanged, this);
    this.model.on('change:position', this.valueChanged, this);
    const cyId = this.model.get('data')['id'];
    this.elem = this.cytoscapeView.cytoscape_obj.getElementById(cyId);
  }
  private _updateClasses() {
    this.elem.classes(this.model.get('classes'));
  }

  valueChanged() {
    this.cytoscapeView.value_changed();
  }
}
