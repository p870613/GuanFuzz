#!/usr/bin/python3
import sys
import matplotlib.pyplot as plt
def main():
    
    if len(sys.argv) < 2:
        print("Usage: ./fuzz_graph.py [queue1_plot_data] [plot_data_label1] [queue2_plot_data] [plot_data_label2]... [title]")
    else:
        for i in range(1, len(sys.argv)-1, 2):
            init_time = 0
            x = []
            y = []
            print(sys.argv[i])
            f = open(sys.argv[i], 'r')
            lines = f.readline()  
            lines = f.readlines()
            f.close()
                
            for line in lines:
                if(init_time == 0):
                    init_time = int(line.split(',', 13)[0].strip()) 
                time = (int(line.split(',', 13)[0].strip()) - init_time) / 3600
                if(time > 12):
                    break
                x.append(time)
                map_size_percentage = line.split(',', 13)[6].strip().replace("%", "")
                map_size = float(map_size_percentage) * 65536 / 100
                y.append(map_size)
            
            
            plt.plot(x, y, label = sys.argv[i+1])

        # naming the x axis
        plt.xlabel('t(Hour)')
        # naming the y axis
        plt.ylabel('edge coverage')
        # giving a title to my graph
        plt.title(sys.argv[len(sys.argv)-1])

        
        # show a legend on the plot
        plt.legend()
        
        # function to show the plot
        plt.show()
if __name__ == "__main__":
    main()

