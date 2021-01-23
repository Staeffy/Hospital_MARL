"""helper to plot data of training and real game 

"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def get_data(folder, file_name, mode):
    df = pd.read_csv(f"{folder}/{file_name}.csv", header=None)

    if mode == "train":
        df.columns = [
            "Round",
            "Doc",
            "Iteration",
            "Patient",
            "Reward",
            "Q_diff",
            "Random action",
            "Sati_doc",
            "Sati_patients",
            "unknown_policy"
        ]

    if mode == "real":
        df.columns = ["Round", "Doc", "Reward", "helping","Sati_doc", "Sati_patients", "unknown_policy"]
    # df.set_index('Round')
    return df


def get_total_doc_rewards(data):
    rewards = data.groupby("Doc")["Reward"].sum()
    return rewards


def plot_reward_difference(data):
    df = data.groupby(["Round", "Doc"]).sum()["Reward"]
    print(df)
    df = df.unstack()
    print(df)

    df = abs(df[0] - df[1])

    plt.plot(df.values)
    plt.title("Reward difference of doc 1 and 2")
    plt.xlabel("iterations")
    plt.ylabel("Reward difference")
    plt.show()

def plot_reward_accumulated(data):
    df = data.groupby(["Round", "Doc"]).sum()["Reward"]
    df = df.unstack()

    df = abs(df[0] + df[1])

    plt.plot(df.values)
    plt.title("Accumulated Rewards of doc 1 and 2")
    plt.xlabel("iterations")
    plt.ylabel("Reward for iteration")
    plt.show()

def plot_reward_seperate(data, players, subtitle, patient_stats):

    df = data.groupby(["Round", "Doc"]).sum()["Reward"]
    df = df.unstack()
    
    df.plot()
    plt.suptitle(f"Rewards {players}")
    plt.title( f"{subtitle}",fontsize=7)
    plt.xlabel("Iteration")
    plt.ylabel("Reward per action")
    plt.figtext(.4,.0, f"{patient_stats}")

    plt.show()

def plot_satisfaction(data, players, subtitle):

    df = data.groupby(["Round", "Doc"]).sum()["Sati_doc"]
    df = df.unstack()

    df.plot()
    plt.suptitle(f"Satisfation levels for {players}")
    plt.title( f"{subtitle}",fontsize=7)
    plt.xlabel("Iteration")
    plt.ylabel("Satisfaction per action")
    plt.figtext(.4,.0, "Satisfaction depends on helping, treating known patients and performing a specialized treatment")

    plt.show()

def plot_policy_knowledge(data, players, subtitle):

    df = data.groupby(["Round", "Doc"]).sum()["unknown_policy"]
    df = df.unstack()

    df.plot()
    plt.suptitle(f"Unknown policy during actions {players}")
    plt.title( f"{subtitle}",fontsize=7)
    plt.xlabel("Iteration")
    plt.ylabel("Amount of unknown best actions")
    #plt.figtext(.4,.0, "")

    plt.show()


def plot_Q_diff(df, title, subtitle):

    # new=df.drop(columns=['Iteration', 'Patient','Reward',''])
    # new.columns = ["Round", "Doc","Q_diff"]
    df = df.groupby(["Round", "Doc"]).sum()["Q_diff"]
    # print(df)
    df = df.unstack()
    df.plot()
    plt.suptitle(f"Q-value difference {title}")
    plt.title( f"{subtitle}",fontsize=7)
    plt.xlabel("Iteration")
    plt.ylabel("Difference between Q-table-values")
    plt.figtext(.4,.0, "Satisfaction depends on helping, treating known patients and performing a specialized treatment")

    plt.show()

def plot_multi_data(x, y, line, data):
    sns.lineplot(x=x, y=y, hue=line, data=data)
    plt.show()

def save_figure(path,name):
    
    plt.savefig(f"{path}/{name}.png")


def plot_random_ratio(data):
    sns.catplot(x="Random action", kind="count", palette="ch:.25", data=data)
    plt.title("Random Ratio")

    plt.show()


if __name__ == "__main__":

    tr = get_data('Strategy_Q_learner_Random','train_2_staff_6_pat_20_treatments','train')
    #rl = get_data("real_game")

    print(tr.head())

    # PLOT REWARD DIFF
    #plot_reward_difference(tr)
    #plot_reward_difference(rl)

    # PLOT REWARD SEPERATE
    plot_reward_seperate(tr, 'test', 'a=x, y=4,m=5')

    #plot_reward_accumulated(rl)

    #plot_reward_accumulated(tr)

    # PLOT Q DIFF
    plot_Q_diff(tr,"random, q_learner","xxxxxxxxxxxxxxxx")



    #rl.columns = ["Round", "Doc", "Reward"]
    #print(rl)

    #r = get_total_doc_rewards(rl)
    #print(r)

    ##COUNT RANDOM ACTIONS
    # ran_act=df.groupby(['Doc']).sum()['Random action']
    # print(ran_act)

    # plot_Q_diff(tr)

    ##PATIENT SEQUENCE
    # patient_seq=df.groupby(['Patient']).sum()['Iteration']
    # print(patient_seq)
