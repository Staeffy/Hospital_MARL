"""helper to plot data of training and real game 

"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def get_data(name):
    df = pd.read_csv("{}.csv".format(name), header=None)

    if name == "training":
        df.columns = [
            "Round",
            "Doc",
            "Iteration",
            "Patient",
            "Reward",
            "Q_diff",
            "Random action",
        ]

    if name == "real_game":
        df.columns = ["Round", "Doc", "Reward"]
    # df.set_index('Round')
    return df


def get_total_doc_rewards(data):
    rewards = data.groupby("Doc")["Reward"].sum()
    return rewards


def plot_reward_difference(data):

    doctors = set(data["Doc"].tolist())

    df = data.groupby(["Round", "Doc"]).sum()["Reward"]
    df = df.unstack()

    doctor_one = df.iloc[:, 0]
    print(doctor_one)
    doctor_two = df.iloc[:, 1]
    print(doctor_two)

    df = abs(doctor_one - doctor_two)

    plt.plot(df.values)
    plt.title(f"Reward difference of {doctors}")
    plt.xlabel("iterations")
    plt.ylabel("Reward difference")
    plt.show()


def plot_reward_seperate(data):
    df = data.groupby(["Round", "Doc"]).sum()["Reward"]
    df = df.unstack()
    df = abs(df[0] + df[1])

    plt.plot(df.values)
    plt.title("Accumulated Rewards of doc 1 and 2")
    plt.xlabel("iterations")
    plt.ylabel("Reward for iteration")
    plt.show()


def plot_reward_accumulated(data):
    df = data.groupby(["Round", "Doc"]).sum()["Reward"]
    df = df.unstack()
    plt.plot(df.values)
    plt.title("Rewards of doc 1 and 2")
    plt.xlabel("iterations")
    plt.ylabel("Reward for iteration")
    plt.show()


def plot_Q_diff(df):

    # new=df.drop(columns=['Iteration', 'Patient','Reward',''])
    # new.columns = ["Round", "Doc","Q_diff"]
    df = df.groupby(["Round", "Doc"]).sum()["Q_diff"]
    # print(df)
    df = df.unstack()
    df.plot()
    plt.title("Q - difference")
    plt.xlabel("iterations")
    plt.ylabel("values")
    plt.show()
    plt.savefig("Q_diff.png")


def plot_multi_data(x, y, line, data):
    sns.lineplot(x=x, y=y, hue=line, data=data)
    plt.show()


def plot_random_ratio(data):
    sns.catplot(x="Random action", kind="count", palette="ch:.25", data=df)
    plt.title("Random Ratio")

    plt.show()


if __name__ == "__main__":

    # tr = get_data("training_simple")
    rl = get_data("real_game")

    print(rl.head())

    # PLOT REWARD DIFF
    # plot_reward_difference(tr)
    plot_reward_difference(rl)

    # PLOT REWARD SEPERATE
    plot_reward_seperate(rl)

    plot_reward_accumulated(rl)

    # plot_reward_accumulated(tr)

    # PLOT Q DIFF
    # plot_Q_diff(tr)

    # rl.columns = ["Round", "Doc", "Reward"]
    print(rl)

    r = get_total_doc_rewards(rl)
    print(r)

    ##COUNT RANDOM ACTIONS
    # ran_act=df.groupby(['Doc']).sum()['Random action']
    # print(ran_act)

    # plot_Q_diff(tr)

    ##PATIENT SEQUENCE
    # patient_seq=df.groupby(['Patient']).sum()['Iteration']
    # print(patient_seq)
