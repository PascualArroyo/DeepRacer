def reward_function(params):

    
    import math

    # Read input variables
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
    

    #1 Position in track, Do not get too close to the limits of the track.

    # Calculate 3 markers that are at varying distances away from the center line.
    marker_1 = 0.35 * track_width
    marker_2 = 0.40 * track_width
    marker_3 = 0.45 * track_width

    # Give higher reward if the agent is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.01
    else:
        reward = 1e-3  # likely crashed/ close to off track


    #2 Anticipate turns to shorten the track.
    tam = len(waypoints)

    #One waypoint forward
    midle_waypoint = closest_waypoints[1]+1
    if midle_waypoint >= tam:
        midle_waypoint = 0

    #Two waypoint forward
    forward_waypoint = closest_waypoints[1]+2
    if forward_waypoint >= tam:
        forward_waypoint = 1

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
        reward *= 0.1
    elif direction_diff > DIRECTION_THRESHOLD_2:
        reward *= 0.4
    elif direction_diff > DIRECTION_THRESHOLD_3:
        reward *= 0.7
        
        
        
    #3 Smoth Steering
    track_direction2 = math.atan2(midle_point[1] - prev_point[1], midle_point[0] - prev_point[0])
    # Convert to degree
    track_direction2 = math.degrees(track_direction2)
        
    ABS_STEERING_THRESHOLD = 40
    if abs(track_direction-track_direction2) > 5:
        ABS_STEERING_THRESHOLD = 20
    # Penalize reward if the agent is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.6
           
           
    #4 Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS1 = 1000
    TOTAL_NUM_STEPS2 = 1075
    TOTAL_NUM_STEPS3 = 1150

    # Give additional reward if the car pass every 100 steps faster than expected
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS1) * 100 :
        reward += 15.0
    elif (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS2) * 100 :
        reward += 10.0
    elif (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS3) * 100 :
        reward += 5.0
        
        
    if speed < 0.7:
        reward *= 0.8
        
    if is_offtrack or is_reversed:
        reward = -10

    return float(reward)
