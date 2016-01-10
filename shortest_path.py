import sys
import vk_api

'''
    Here is script for searching a shortest path (by friends)
    between two people in vkontakte.

    It uses BFS, but from two points, we detect the first moment
    of paths intersection from the first men and the second

    In the tree structure we store paths from the first or the second men
    
    Cause Vk limits on requests it can take some time (up to 1-2 minuets)
'''


class Tree:
    def __init__(self, root):
        self.root = root
        self.nodes = {root: -1}
        self.grays = {root}

    def join(self, parent, child):
        if child not in self.nodes:
            self.nodes[child] = parent
            self.grays.add(child)

    def path_up(self, node, reverse=False):
        if node in self.nodes:
            path = []
            while node != -1:
                path += [node]
                node = self.nodes[node]
            if reverse:
                return path.reverse()
            else:
                return path
        else:
            return []


def vk_find_smallest_path(first_id, second_id, vk):
    first_tree = Tree(first_id)
    second_tree = Tree(second_id)

    """We let if there is not path less than of 100 handshakes, than no path exists at all"""
    max_tries = 100
    for tries in range(max_tries):
        common_friends = list(first_tree.grays.intersection(second_tree.grays))
        if len(common_friends) != 0:
            friend = common_friends[0]
            return first_tree.path_up(friend)[-1:0:-1] + second_tree.path_up(friend)
        else:
            trees = (first_tree, second_tree)
            if len(first_tree.grays) > len(second_tree.grays):
                trees = (second_tree, first_tree)

            new_friends = {}
            for uid in trees[0].grays:
                try:
                    user_friends = vk.method('friends.get', {'user_id': uid})['items']
                    for friend in user_friends:
                        if friend not in trees[0].nodes and friend not in new_friends:
                            new_friends[friend] = uid
                except Exception as e:
                    pass

            trees[0].grays = set(new_friends.keys())
            trees[0].nodes.update(new_friends)

    raise Exception("no path exists")


def main():
    login, password = "your_login", "your_password"
    vk = vk_api.VkApi(login, password)

    try:
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    first_id = int(sys.stdin.readline())
    second_id = int(sys.stdin.readline())

    try:
        user_ids = ','.join([str(u_id) for u_id in vk_find_smallest_path(first_id, second_id, vk)])
    except Exception as e:
        print("sorry, no path")
        return

    chain = vk.method('users.get', {'user_ids': user_ids})
    for user in chain:
        print(user)

if __name__ == '__main__':
    main()