import numpy as np
import matplotlib.pyplot as plt

def plot_imu_data(accels, gyros, magnets = None, time=None, imu_n=0, axs=None, fig=None, labels=None, titles=None, measurement_units=None):
    N = max(accels.shape)
    if time is None:
        t_end = 10
        t_span = np.linspace(0, t_end, N)

    if type(time) is float:
        t_span = np.linspace(0, time, N)

    t_span = time
    if axs is None or fig is None:
        if magnets is not None:
            ncols, nrows = 1, 3
        else:
            ncols, nrows = 1, 2
        fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(18 * 2, 6 * nrows))
    linestyles: list[str] = ['solid', 'dashed', 'dotted', 'dashdot']

    for ax in axs:
        ax.clear()
    
    if labels is None:
        labels = ["a_x", "a_y", "a_z", "g_x", "g_y", "g_z", "m_x", "m_y", "m_z"]
    if titles is None:
        titles = [f"Acceleration {imu_n}", f"Gyroscopes {imu_n}", f"Magnetometer {imu_n}"]
    if measurement_units is None:
        measurement_units = ["acceleration, rad/s^2","velocity, rad/s", "magnetic flux density, e-6 T"]

    plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
    
    axs[0].title.set_text(titles[0])
    axs[0].plot(t_span, accels[:, 0], label=labels[0], linestyle=linestyles[0])
    axs[0].plot(t_span, accels[:, 1], label=labels[1], linestyle=linestyles[1])
    axs[0].plot(t_span, accels[:, 2], label=labels[2], linestyle=linestyles[2])
    axs[0].set_xlabel("t, s")
    axs[0].set_ylabel(measurement_units[0])
    axs[0].legend()


    axs[1].title.set_text(titles[1])
    axs[1].plot(t_span, gyros[:, 0], label=labels[3], linestyle=linestyles[0])
    axs[1].plot(t_span, gyros[:, 1], label=labels[4], linestyle=linestyles[1])
    axs[1].plot(t_span, gyros[:, 2], label=labels[5], linestyle=linestyles[2])
    axs[1].set_xlabel("t, s")
    axs[1].set_ylabel(measurement_units[1])
    axs[1].legend()

    if magnets is not None:
        axs[2].title.set_text(titles[2])
        axs[2].plot(t_span, magnets[:, 0], label=labels[6], linestyle=linestyles[0])
        axs[2].plot(t_span, magnets[:, 1], label=labels[7], linestyle=linestyles[1])
        axs[2].plot(t_span, magnets[:, 2], label=labels[8], linestyle=linestyles[2])
        axs[2].set_xlabel("t, s")
        axs[2].set_ylabel(measurement_units[2])
        axs[2].legend()

    plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0)
    fig.canvas.draw()
    fig.canvas.flush_events()
    return fig, axs