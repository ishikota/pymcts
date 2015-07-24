import pdb
class Reader:

    def read_board(self, f_name, model):
        """ read board state from specified file and returns updated model

        Args:
            f_name: file name of .in file(file extension inclusive).
                ex) sample.in
            model: model object of connectfour to update

        Returns:
            ans: answer action of test
            model: updated model which passed as args
            next_player: next player of game which read from .in file.
        """

        table = [[0 for j in range(model.WIDTH)] for i in range(model.HEIGHT)]
        position = [model.HEIGHT for i in range(model.WIDTH)]
        count1, count2 = 0, 0
        ans = -1

        f = open(f_name, 'r')
        row = 0
        while row != model.HEIGHT:
            tmp = f.readline()
            # skip the comment or brank line
            if len(tmp)==0 or tmp[0] =='#':
                continue
            elif tmp[:3] == 'ans':
                tmp2, ans = tmp.split(':')
                ans = map(int, ans.split(','))
                continue
            
            line = tmp.split()
            for col in range(model.WIDTH):
                line[col] = 0 if line[col]=='-' else 1 if line[col]=='O' else -1
                table[model.HEIGHT-1-row][col] = line[col]
                if line[col] == 1: # 1 is the move of first player
                    count1 += 1
                elif line[col] == -1: # -1 is the move of second player
                    count2 += 1
                else:
                    position[col] = min(position[col], (model.HEIGHT-1-row))
            row += 1
        model.table = table
        model.position = position
        next_player = 1 if count1==count2 else -1
        return ans, model, next_player


