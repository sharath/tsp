import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import sys

def euclid(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(0.5)

def dist(xp):
    fv = 0
    for i in range(1, len(xp[0])):
        fv += euclid((xp[0][i-1], xp[1][i-1]), (xp[0][i], xp[1][i]))
    return fv

def permute(xp):
    t = eval(str(xp))
    i = int(np.random.randint(1, len(t[0])-3))
    t[0][i], t[1][i], t[0][i+1], t[1][i+1] = t[0][i+1], t[1][i+1], t[0][i], t[1][i]
    return t


def simulated_annleaing(T=3, points=15, dim=20, T_bound=1e-4, T_decay=0.01, T_schedule='linear', max_iter=np.inf, seed=0):
    np.random.seed(seed)
    xc = (np.random.rand(2, points)*dim).tolist()
    
    xc[0].append(xc[0][0])
    xc[1].append(xc[1][0])
    
    paths = [xc]
    bf = [dist(xc)]
    temps = [T]
    iterations = [0]
    prob =[1]
    
    while T > T_bound:
        xp = permute(xc)
        prob_a = None
        if dist(xp) < dist(xc):
            xc = xp
        else:
            u = np.random.uniform(0, 1)
            p = np.exp(-1*(dist(xp) - dist(xc))/T)
            prob_a = p
            if p > u:
                xc = xp
        if T_schedule == 'linear':
            T -= T_decay
        elif T_schedule == 'exp':
            T *= T_decay
            T = max(T, T_bound+sys.float_info.epsilon)
        prob.append(prob_a)
        bf.append(dist(xc))
        paths.append(xc)
        temps.append(max(T, 0))
        iterations.append(iterations[-1]+1)
        if iterations[-1] == max_iter:
            break
        
            
    return iterations, paths, bf, temps, prob

def rec(args):
    i, paths, bf, temps, prob  = args['it'], args['paths'], args['bf'], args['temps'], args['prob']
    plt.clf()
    plt.subplot('221')
    plt.title(f'Path at Temperature {temps[i]:.4f}')
    plt.scatter(*paths[i], color='r', zorder=1000)
    plt.plot(*paths[i], color='b')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    plt.subplot('222')
    plt.plot(bf[:i], color='r')
    plt.title('Total Distance')
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    
    plt.subplot('223')
    plt.scatter(list(range(i)), prob[:i], color='g', marker='*')
    plt.title('Acceptance Probability')
    plt.ylim(-0.2, 1.2)
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.xlabel('Iteration')
    plt.ylabel('Probability')
    
    plt.subplot('224')
    plt.title('Temperature Schedule')
    plt.plot(list(range(i)), temps[:i], color='orange')
    plt.xlabel('Iteration')
    plt.ylabel('Temperature')
    
    plt.savefig(f'out/{i:05d}.png')
    print(f'Iteration {i}')

def main():
    plt.rcParams["figure.figsize"] = (10, 10)
    iterations, paths, bf, temps, prob  = iterations, paths, bf, temps, prob = simulated_annleaing(T=50, points=10, dim=10, T_bound=0.002, T_decay=0.999, max_iter=10000, T_schedule='exp', seed=0)
    
    p = Pool(20)
    
    m = []
    for i in iterations:
        args = {}
        args['it'] = i
        args['paths'] = paths
        args['bf'] = bf
        args['temps'] = temps
        args['prob'] = prob
        m.append(args)
        
    p.map(rec, m)
        
if __name__ == '__main__':
    main()