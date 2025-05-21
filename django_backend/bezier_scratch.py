import numpy as np
import csv


def bezier_curve(control_points, num_points=100):
    n = len(control_points) - 1
    t = np.linspace(0, 1, num_points)

    def bernstein_poly(i, n, t):
        return (
            (
                np.emath.factorial(n)
                / (np.emath.factorial(i) * np.emath.factorial(n - i))
            )
            * (t**i)
            * ((1 - t) ** (n - i))
        )

    curve_points = np.array(
        [
            [
                sum(
                    bernstein_poly(i, n, t) * control_points[i][j] for i in range(n + 1)
                )
                for j in range(2)
            ]
            for t in t
        ]
    )
    return curve_points


# Define control points for the Bezier curve
control_points = np.array([[0, 0], [1, 2], [3, 1], [4, 3]])

# Calculate points on the Bezier curve
curve_points = bezier_curve(control_points)

# Save the points to a CSV file
csv_file_path = "bezier_curve_points.csv"
with open(csv_file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["x", "y"])  # Write header row
    writer.writerows(curve_points)

print(f"Bezier curve points saved to {csv_file_path}")
