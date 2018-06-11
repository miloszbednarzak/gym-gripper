import gym
import gym_gripper
from baselines import deepq

import baselines.common.atari_wrappers as atari_wrappers


class Wrapper(atari_wrappers.LazyFrames):

    def wrap_deepmind(env, episode_life=False, clip_rewards=True, frame_stack=True, scale=True):
        """Configure environment for DeepMind-style Atari.
        """
        if episode_life:
            env = atari_wrappers.EpisodicLifeEnv(env)
        env = atari_wrappers.WarpFrame(env)
        if scale:
            env = atari_wrappers.ScaledFloatFrame(env)
        if clip_rewards:
            env = atari_wrappers.ClipRewardEnv(env)
        if frame_stack:
            env = atari_wrappers.FrameStack(env, 4)
        return env


def main():
    env = gym.make('Gripper2D-v0')
    env = Wrapper.wrap_deepmind(env)
    model = deepq.models.cnn_to_mlp(convs=[(32, 8, 4),
                                           (64, 4, 2),
                                           (64, 3, 1)],
                                    hiddens=[256],
                                    layer_norm=True)
    act = deepq.learn(env,
                      model,
                      )

    act.save("gripper_model.pkl")
    env.close()


if __name__ == '__main__':
    main()
