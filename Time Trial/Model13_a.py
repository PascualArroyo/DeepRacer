def reward_function(params):

    import math
    # Read input variables
   
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    steps = params['steps']
    progress = params['progress']
    speed = params['speed']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
   
    objects_distance = params['objects_distance']
    _, next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']


    # Initialize reward with a small number but not zero
    # because zero means off-track or crashed
    reward = 1e-3
   
   
    #1 Position in track, Do not get too close to the limits of the track.
    # Reward if the agent stays inside the two borders of the track
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward_lane = 1.0
    elif distance_from_center <= marker_2:
        reward_lane = 0.5
    elif distance_from_center <= marker_3:
        reward_lane = 0.1
    else:
        reward_lane = 1e-3  # likely crashed/ close to off track


    #2 Anticipate turns to shorten the track.
    tam = len(waypoints)

    #One waypoint forward
    midle_waypoint = closest_waypoints[1]+8
    if midle_waypoint >= tam:
        midle_waypoint = 8

    #Two waypoint forward
    forward_waypoint = closest_waypoints[1]+16
    if forward_waypoint >= tam:
        forward_waypoint = 16


    # Points of track
    forward_point = waypoints[forward_waypoint]
    midle_point = waypoints[midle_waypoint]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction of the center line based on the closest waypoints
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(forward_point[1] - prev_point[1], forward_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD_1 = 12.0
    DIRECTION_THRESHOLD_2 = 8.0
    DIRECTION_THRESHOLD_3 = 4.0

    if direction_diff > DIRECTION_THRESHOLD_1:
        reward_direction = 1e-3
    elif direction_diff > DIRECTION_THRESHOLD_2:
        reward_direction = 0.3
    elif direction_diff > DIRECTION_THRESHOLD_3:
        reward_direction = 0.8
    else:
        reward_direction = 1
 
 
 
 
 

    #3 Smoth Steering
    track_direction2 = math.atan2(midle_point[1] - prev_point[1], midle_point[0] - prev_point[0])
    # Convert to degree
    track_direction2 = math.degrees(track_direction2)
   

    ABS_STEERING_THRESHOLD = 20
    
    if abs(track_direction-track_direction2) < 5:
        # Penalize reward if the agent is steering too much
        if steering > ABS_STEERING_THRESHOLD:
            reward_sterring = 0
        else:
            reward_sterring = 1
           
    elif abs(track_direction-track_direction2) < 12:
        # Penalize reward if the agent is steering too much
        if steering > ABS_STEERING_THRESHOLD:
            reward_sterring = 0.5
        else:
            reward_sterring = 1
   
    else:
        # Penalize reward if the agent is steering too much
        # Penalize reward if the agent is steering too much
        if steering > ABS_STEERING_THRESHOLD:
            reward_sterring = 0.8
        else:
            reward_sterring = 1



    #4 Speed depends of steering
    if steering > ABS_STEERING_THRESHOLD:
        if speed > 3:
            reward_speed = -1
        elif speed > 2:
            reward_speed = -0.5
        else:
            reward_speed = 1
       
    else:
        if speed > 3:
            reward_speed = -1
        elif speed > 2:
            reward_speed = 0.5
        else:
            reward_speed = 1
  
  


    #5 Optimize track
    TOTAL_NUM_STEPS1 = 450
    TOTAL_NUM_STEPS2 = 460
    TOTAL_NUM_STEPS3 = 470
    TOTAL_NUM_STEPS4 = 480
    TOTAL_NUM_STEPS5 = 490
    TOTAL_NUM_STEPS6 = 500
    TOTAL_NUM_STEPS7 = 520
    TOTAL_NUM_STEPS8 = 540
    TOTAL_NUM_STEPS9 = 560
    TOTAL_NUM_STEPS10 = 580
     
     
    # Give additional reward if the car pass every 50 steps faster than expected
    reward_optimize = 0

    if (steps % 50) == 0:
        if progress > (steps / TOTAL_NUM_STEPS1) * 100 :
            reward_optimize = 60
        elif progress > (steps / TOTAL_NUM_STEPS2) * 100 :
            reward_optimize = 50
        elif progress > (steps / TOTAL_NUM_STEPS3) * 100 :
            reward_optimize = 40
        elif progress > (steps / TOTAL_NUM_STEPS4) * 100 :
            reward_optimize = 30
        elif progress > (steps / TOTAL_NUM_STEPS5) * 100 :
            reward_optimize = 25
        elif progress > (steps / TOTAL_NUM_STEPS6) * 100 :
            reward_optimize = 20
        elif progress > (steps / TOTAL_NUM_STEPS7) * 100 :
            reward_optimize = 15
        elif progress > (steps / TOTAL_NUM_STEPS8) * 100 :
            reward_optimize = 10
        elif progress > (steps / TOTAL_NUM_STEPS9) * 100 :
            reward_optimize = 5
        elif progress > (steps / TOTAL_NUM_STEPS10) * 100 :
            reward_optimize = 1
        else :
            reward_optimize = 0


    # Calculate reward by putting different weights
    reward += 1.0 * reward_lane + 1.0 * reward_direction + 1.0 * reward_sterring + 1.0 * reward_speed + reward_optimize
   
 
    return float(reward)
