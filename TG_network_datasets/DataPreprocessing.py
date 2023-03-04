def create_dataset():
    print("creating dataset")
    # with open(data_name) as f:
    #     s = next(f)  # skip the first line
    #     for idx, line in enumerate(f):
    #       e = line.strip().split(',')
    #       u = int(e[0])  # user_id
    #       i = int(e[1])  # item_id
    #
    #       ts = float(e[2])  # timestamp  --> assumed in ascending order (I've checked it)
    #       label = float(e[3])  # int(e[3])  # state_label
    #
    #       feat = np.array([float(x) for x in e[4:]] + [0 for _ in range(n_node_feat - (4+1))])  # edge features
    #
    #       u_list.append(u)
    #       i_list.append(i)
    #       ts_list.append(ts)
    #       label_list.append(label)
    #       idx_list.append(idx)
    #
    #       feat_l.append(feat)


if __name__ == "__main__":
    paper_data = dict()
    paper_map = dict()
    create_dataset()