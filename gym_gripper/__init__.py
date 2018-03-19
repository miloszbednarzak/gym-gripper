from gym.envs.registration import register

register(
    id='gripper2d-v0',
    entry_point='gym_gripper.envs:Gripper2DEnv',
)