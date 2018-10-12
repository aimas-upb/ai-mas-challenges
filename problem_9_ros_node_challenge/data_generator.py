import numpy as np
import math, csv
import matplotlib.pyplot as plt

DISTANCE = 10
ANGLE = np.pi / 4;

AXIS_ROT_ANGLE = -np.pi / 2;
AXIS_TRANS = np.array([10, 0])

MEAN_SENSOR = np.array([DISTANCE, ANGLE])
COVARIANCE_SENSOR = np.array([[0.75 * 0.75, 0], [0, (np.pi / 90) * (np.pi / 90)]])

if __name__ == "__main__":
    samples_dist = np.random.multivariate_normal(MEAN_SENSOR, COVARIANCE_SENSOR, 100)

    # plt.boxplot([180 * s[1] / np.pi for s in samples_dist])

    samples_x = [d * math.cos(theta) for [d, theta] in samples_dist]
    samples_y = [d * math.sin(theta) for [d, theta] in samples_dist]

    samples_coord = [np.array(list(coords)) for coords in zip(samples_x, samples_y)]

    rotation_matrix = np.array(
        [[math.cos(AXIS_ROT_ANGLE), math.sin(AXIS_ROT_ANGLE)],
         [-math.sin(AXIS_ROT_ANGLE), math.cos(AXIS_ROT_ANGLE)],
        ]
    )
    trans_new_coord = np.matmul(AXIS_TRANS, rotation_matrix)

    mean_sensor_x = DISTANCE * math.cos(ANGLE)
    mean_sensor_y = DISTANCE * math.sin(ANGLE)

    mean_sensor_rotated = np.matmul(np.array([mean_sensor_x, mean_sensor_y]), rotation_matrix)
    mean_sensor_transformed = np.array([mean_sensor_rotated[0] - trans_new_coord[0],
                                        mean_sensor_rotated[1] - trans_new_coord[1]]
                                       )
    mean_sensor_transformed_dist = np.array( [np.linalg.norm(mean_sensor_transformed),
                                              math.atan2(mean_sensor_transformed[1], mean_sensor_transformed[0])]
                                             )

    samples_transformed_dist = np.random.multivariate_normal(mean_sensor_transformed_dist, COVARIANCE_SENSOR, 100)
    plt.boxplot([180 * s[1] / np.pi for s in samples_transformed_dist])
    plt.show()

    # samples_rotated = [np.matmul(s, rotation_matrix) for s in samples_coord]
    # samples_transformed_dist = [np.array([s[0] - trans_new_coord[0], s[1] - trans_new_coord[1]]) for s in samples_rotated]

    # samples_transformed_x = [s[0] for s in samples_transformed_dist]
    # samples_transformed_y = [s[1] for s in samples_transformed_dist]
    #
    # samples_transformed_dist = [np.array( [np.linalg.norm(s), math.atan2(s[1], s[0])] ) for s in samples_transformed_dist]
    # plt.boxplot([180 * s[1] / np.pi for s in samples_transformed_dist])

    # fig1, ax1 = plt.subplots()
    # ax1.set_title("Points in original axis")
    # ax1.scatter(samples_x, samples_y)
    #
    # fig2, ax2 = plt.subplots()
    # ax2.set_title("Points in transformed axis")
    # ax2.scatter(samples_transformed_x, samples_transformed_y)

    fieldnames = ['distance', 'angle']

    with open("data/sensor1.csv", mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames= fieldnames)
        writer.writeheader()

        for s in samples_dist:
            writer.writerow({
                'distance': round(s[0], 4),
                'angle': round(s[1], 4)
            })

    with open("data/sensor2.csv", mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for s in samples_transformed_dist:
            writer.writerow({
                'distance': round(s[0], 4),
                'angle': round(s[1], 4)
            })


    test_distances = np.random.uniform(low=2.5, high=10.5, size=(10,))
    test_angles = np.random.uniform(low = np.pi / 30, high = 2 * np.pi / 3, size=(10,))

    test_points = [np.array([e[0], e[1]]) for e in zip(test_distances, test_angles)]
    test_points_coords = [ np.array([ e[0] * math.cos(e[1]), e[0] * math.sin(e[1]) ]) for e in test_points]

    test_points_rotated = [np.matmul(s, rotation_matrix) for s in test_points_coords]
    test_points_transformed = [np.array([s[0] - trans_new_coord[0], s[1] - trans_new_coord[1]]) for s in test_points_rotated]

    # plt.scatter([s[0] for s in test_points_coords], [s[1] for s in test_points_coords])
    # plt.scatter([s[0] for s in test_points_transformed], [s[1] for s in test_points_transformed])

    test_points_transformed_dist = [np.array( [np.linalg.norm(s), math.atan2(s[1], s[0])] ) for s in test_points_transformed]

    with open("data/test_sensor1.csv", mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for s in test_points:
            writer.writerow({
                'distance': round(s[0], 4),
                'angle': round(s[1], 4)
            })

    with open("data/test_sensor2.csv", mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for s in test_points_transformed_dist:
            writer.writerow({
                'distance': round(s[0], 4),
                'angle': round(s[1], 4)
            })
