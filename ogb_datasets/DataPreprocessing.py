from ogb.graphproppred import PygGraphPropPredDataset
from torch_geometric.data import DataLoader
import networkx as nx


# Download and process data at './dataset/ogbg_molhiv/'
dataset = PygGraphPropPredDataset(name="ogbg-molhiv", root='dataset/')
graph = nx.to_networkx_graph(dataset[0])


split_idx = dataset.get_idx_split()
train_loader = DataLoader(dataset[split_idx["train"]], batch_size=32, shuffle=True)
valid_loader = DataLoader(dataset[split_idx["valid"]], batch_size=32, shuffle=False)
test_loader = DataLoader(dataset[split_idx["test"]], batch_size=32, shuffle=False)

