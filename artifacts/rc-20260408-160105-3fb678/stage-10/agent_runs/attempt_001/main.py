# config.py

"""
Hyperparameter configuration for the toroidal vortex geometry experiment.
All tunable parameters are defined here and used throughout the pipeline.
"""

HYPERPARAMETERS = {
    'seed': 42,
    'num_seeds': 3,
    'batch_size': 64,
    'lr': 0.001,
    'epochs': 25,
    'hidden_dim': 128,
    'num_materials': 5000,
    'feat_dim': 64,
    'num_platonic_classes': 5,
    'num_magnetic_classes': 3,
    'train_ratio': 0.7,
    'val_ratio': 0.15,
    'test_ratio': 0.15,
    'time_budget_seconds': 300,
    'device': 'auto',
    'weight_decay': 1e-5,
    'patience': 8,
    'max_grad_norm': 1.0,
    'w_susceptibility': 1.0,
    'w_conductivity': 0.8,
    'w_hardness': 0.8,
    'w_melting_point': 0.8,
    'w_magnetic_class': 1.5,
    'w_vortex_coherence': 0.5,
    'w_platonic_aux': 0.3,
    'w_smoothness': 0.1,
    'w_icosahedral_anomaly': 0.5,
    'w_cross_scale': 0.3,
    'w_alignment': 0.5,
    'w_ferro_cls': 1.0,
    'w_consistency': 0.3,
    'feat_crystal_onehot': 7,
    'feat_platonic_subgroups': 5,
    'feat_vortex_topology': 8,
    'feat_point_group': 1,
    'feat_coordination': 1,
    'feat_packing': 1,
    'feat_topological': 4,
    'feat_space_embed': 37,
}


class Config:
    """Configuration container for all experiment hyperparameters."""
    def __init__(self, **overrides):
        for k, v in HYPERPARAMETERS.items():
            setattr(self, k, overrides.get(k, v))

    @property
    def feat_dim(self):
        return (self.feat_crystal_onehot + self.feat_platonic_subgroups +
                self.feat_vortex_topology + self.feat_point_group +
                self.feat_coordination + self.feat_packing +
                self.feat_topological + self.feat_space_embed)

    def get_device(self):
        import torch
        if self.device == 'auto':
            if torch.cuda.is_available():
                return torch.device('cuda')
            try:
                if torch.backends.mps.is_available():
                    return torch.device('mps')
            except Exception:
                pass
            return torch.device('cpu')
        return torch.device(self.device)

    def get_seed_list(self):
        return [0, 1, 2][:self.num_seeds]