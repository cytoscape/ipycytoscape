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
      removed: false,
      selected: false,
      selectable: true,
      classes: '',
      data: {},
    };
  }
  asCyObj() {
    return {
      data: this.get('data'),
      selectable: this.get('selectable'),
      classes: this.get('classes'),
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

      group: 'nodes',
      position: {},
      locked: false,
      grabbable: false,
      pannable: false,
    };
  }

  asCyObj() {
    return {
      ...super.asCyObj(),
      group: this.get('group'),
      position: this.get('position'),
      locked: this.get('locked'),
      grabbable: this.get('grabbable'),
      pannable: this.get('pannable'),
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

      group: 'edges',
      pannable: true,
    };
  }

  asCyObj() {
    return {
      ...super.asCyObj(),
      group: this.get('group'),
      pannable: this.get('pannable'),
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

    this.model.on('change:removed', this.valueChanged, this);
    this.model.on('change:classes', () => {
      this.elem.classes(this.model.get('classes'));
    });
    this.model.on('change:data', () => {
      this.elem.data(this.model.get('data'));
    });
    this.model.on('change:pannable', () => {
      // I think @types/cytoscape is missing panify and unpanify
      this.model.get('pannable')
        ? (this.elem as any).panify()
        : (this.elem as any).unpanify();
    });
    this.model.on('change:selectable', () => {
      this.model.get('selectable')
        ? this.elem.selectify()
        : this.elem.unselectify();
    });
    this.model.on('change:selected', () => {
      this.model.get('selected')
        ? this.elem.selectify()
        : this.elem.unselectify();
    });
  }

  valueChanged() {
    this.cytoscapeView.value_changed();
  }
}
export class NodeView extends ElementView {
  private node: NodeSingular;
  constructor(params: any) {
    super({
      model: params.model,
      options: params.options,
    });
    this.node = this.elem as NodeSingular;
    this.model.on('change:position', () => {
      this.node.position(this.model.get('position'));
    });
    this.model.on('change:locked', () => {
      this.model.get('locked') ? this.node.lock() : this.node.unlock();
    });
    this.model.on('change:grabbable', () => {
      this.model.get('grabbable') ? this.node.grabify() : this.node.ungrabify();
    });
  }
}

export class EdgeView extends ElementView {
  //   private edge: EdgeSingular;
  constructor(params: any) {
    super({
      model: params.model,
      options: params.options,
    });
    // this.edge = this.elem as EdgeSingular;
  }
}
