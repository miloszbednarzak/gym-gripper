from gym.envs.registration import register

register(
    id='Gripper2D-v0',
    entry_point='gym_gripper.envs:Gripper2DEnv',
)