# position of the ball on the plane board
float64 x #(m)
float64 y #(m)
float64 z #(m)

# position of the ball in the previous frame
float64 x2 #(m)
float64 y2 #(m)
float64 z2 #(m)

# position of the ball in the previous previous frame
float64 x3 #(m)
float64 y3 #(m)
float64 z3 #(m)

# postiion of the waypoint 
float64 x_way #(m)
float64 y_way #(m)
float64 z_way #(m)

# lists of previous ball/waypoint coords
float64[] ball_coord
float64[] way_coord
float64[] way2_coord

# position of the border
int32[] border