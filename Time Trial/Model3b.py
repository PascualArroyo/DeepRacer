def reward_function(params):

    
    import math

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle


   # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.40 * track_width
    marker_2 = 0.45 * track_width
    marker_3 = 0.49 * track_width

    # Give higher reward if the agent is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.6
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15

    # Penalize reward if the agent is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    tam = len(waypoints)

    #Two waypoint forward
    next_waypoint = closest_waypoints[1]+2
    if next_waypoint >= tam:
        next_waypoint = 1

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[next_waypoint]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD_1 = 10.0
    DIRECTION_THRESHOLD_2 = 6.0
    DIRECTION_THRESHOLD_3 = 3.0
    
    if direction_diff > DIRECTION_THRESHOLD_1:
        reward *= 0.2
    elif direction_diff > DIRECTION_THRESHOLD_2:
        reward *= 0.5
    elif direction_diff > DIRECTION_THRESHOLD_3:
        reward *= 0.8


    return float(reward)
