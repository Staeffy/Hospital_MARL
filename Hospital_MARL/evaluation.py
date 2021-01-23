import play
import train
import rl_setup
import stats 


if __name__ == "__main__":



    patients = rl_setup.load_json("patient_list_many_treatments")
    doc_stats = rl_setup.load_json("doc_stats_train")

    #variations=[0.1,0.5,0.8,1]
    variations=[0.1,0.5]
    learning_stats=doc_stats['doc1']['learning']
    reward_stats=doc_stats['doc1']['preferences']

    for stat in learning_stats:
        for param in variations:

            learning_stats[stat]=param

            rounds=10000

            #TRAIN 
            folder_name, file_name, initialized_names = train.train(patients, doc_stats, rounds)
            data=stats.get_data('stats/'+folder_name, file_name, 'train')
            stats.plot_Q_diff(data, initialized_names, learning_stats)
            stats.plot_policy_knowledge(data, initialized_names, learning_stats)

            #REAL 
            rounds=5
            file_name = play.play(patients, doc_stats, folder_name, rounds)
            data=stats.get_data('stats/'+folder_name, file_name, 'real')
            stats.plot_reward_seperate(data, initialized_names, reward_stats, file_name)
            stats.plot_satisfaction(data, initialized_names, file_name)
            s

            # print(f"doc variables {doc_stats}")
            # print(f"parameter to be changed is {stat} with param{param}")



