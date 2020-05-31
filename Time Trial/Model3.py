def reward_function(params):

    
    import math

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle


    #Init reward
    reward = 1

    # Calculate 3 markers that are at varying distances away from the center line
    marker = 0.48 * track_width

    if distance_from_center >= marker:
        reward *= 0.05
    
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
    DIRECTION_THRESHOLD_2 = 5.0
    DIRECTION_THRESHOLD_3 = 2.0
    
    if direction_diff > DIRECTION_THRESHOLD_1:
        reward *= 0.1
    elif direction_diff > DIRECTION_THRESHOLD_2:
        reward *= 0.5
    elif direction_diff > DIRECTION_THRESHOLD_3:
        reward *= 0.8


    return float(reward)
