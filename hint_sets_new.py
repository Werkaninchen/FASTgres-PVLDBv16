
# def set_hints(hint_set, cursor):
#     for i in range(hint_set.hint_set_size):
#         name = hint_set.get_name(i)
#         value = hint_set.get(i)
#         statement = 'set {}={};'.format(name, value)
#         cursor.execute(statement)
#     return hint_set


# def show_hint_status(cursor):
#     operators = HintSet.operators
#     for i in operators:
#         statement = 'show {};'.format(i)
#         cursor.execute(statement)
#         res = cursor.fetchall()[0][0]
#         print('{} is set to "{}"'.format(i, res))
#     print('\n')
#     return


# def reset_hints(cursor):
#     reset_operators = HintSet.operators
#     for operator in reset_operators:
#         statement = 'set ' + operator + '=true;'
#         cursor.execute(statement)
#     return


# class HintSet:

#     operators = [
#         'enable_async_append',  # 8192
#         'enable_parallel_append',  # 4096
#         'enable_parallel_hash',  # 2048
#         'enable_sort',  # 1024
#         'enable_bitmapscan',  # 512
#         'enable_memoize',  # 256
#         "enable_gathermerge",  # 128
#         "enable_hashagg",  # 64
#         "enable_incremental_sort",  # 32
#         "enable_material",  # 16,
#         "enable_partition_pruning",  # 8
#         "enable_partitionwise_join",  # 4
#         "enable_partitionwise_aggregate",  # 2
#         "enable_tidscan",  # 1
#     ]

#     def __init__(self, default: int = None):
#         self.enable_async_append = True
#         self.enable_parallel_append = True
#         self.enable_parallel_hash = True
#         self.enable_sort = True
#         self.enable_bitmapscan = True
#         self.enable_memoize = True
#         self.enable_gathermerge = True
#         self.enable_hashagg = True
#         self.enable_incremental_sort = True
#         self.enable_material = True
#         self.enable_partition_pruning = True
#         self.enable_partitionwise_join = True
#         self.enable_partitionwise_aggregate = True
#         self.enable_tidscan = True
#         self.hint_set_size = len(HintSet.operators)

#         if default is not None:
#             if not isinstance(default, int):
#                 raise ValueError('Input hint set is not of type int')
#             self.set_hint_from_int(default)

#         return

#     def set_hint_from_int(self, hint_int):
#         binary_list = [int(i) for i in bin(hint_int)[
#             2:].zfill(self.hint_set_size)]
#         self.set_from_int_list(binary_list)
#         return

#     def set_hint_i(self, i, value):
#         if value not in [True, False]:
#             raise ValueError('Trying to set hint set from non boolean')
#         else:
#             if i == 0:
#                 self.enable_async_append = value
#             elif i == 1:
#                 self.enable_parallel_append = value
#             elif i == 2:
#                 self.enable_parallel_hash = value
#             elif i == 3:
#                 self.enable_sort = value
#             elif i == 4:
#                 self.enable_bitmapscan = value
#             elif i == 5:
#                 self.enable_memoize = value
#             elif i == 6:
#                 self.enable_gathermerge = value
#             elif i == 7:
#                 self.enable_hashagg = value
#             elif i == 8:
#                 self.enable_incremental_sort = value
#             elif i == 9:
#                 self.enable_material = value
#             elif i == 10:
#                 self.enable_partition_pruning = value
#             elif i == 11:
#                 self.enable_partitionwise_join = value
#             elif i == 12:
#                 self.enable_partitionwise_aggregate = value
#             elif i == 13:
#                 self.enable_tidscan = value
#             else:
#                 raise ValueError('Invalid Index')
#         return

#     def print_info(self):
#         print('enable_async_append:', self.enable_async_append)
#         print('enable_parallel_append:', self.enable_parallel_append)
#         print('enable_parallel_hash:', self.enable_parallel_hash)
#         print('enable_sort:', self.enable_sort)
#         print('enable_bitmapscan:', self.enable_bitmapscan)
#         print('enable_memoize:', self.enable_memoize)
#         print('enable_gathermerge:', self.enable_gathermerge)
#         print('enable_hashagg:', self.enable_hashagg)
#         print('enable_incremental_sort:', self.enable_incremental_sort)
#         print('enable_material:', self.enable_material)
#         print('enable_partition_pruning:', self.enable_partition_pruning)
#         print('enable_partitionwise_join:', self.enable_partitionwise_join)
#         print('enable_partitionwise_aggregate:',
#               self.enable_partitionwise_aggregate)
#         print('enable_tidscan:', self.enable_tidscan)
#         print('\n')
#         return

#     def get(self, i):
#         if i == 0:
#             return self.enable_async_append
#         elif i == 1:
#             return self.enable_parallel_append
#         elif i == 2:
#             return self.enable_parallel_hash
#         elif i == 3:
#             return self.enable_sort
#         elif i == 4:
#             return self.enable_bitmapscan
#         elif i == 5:
#             return self.enable_memoize
#         elif i == 6:
#             return self.enable_gathermerge
#         elif i == 7:
#             return self.enable_hashagg
#         elif i == 8:
#             return self.enable_incremental_sort
#         elif i == 9:
#             return self.enable_material
#         elif i == 10:
#             return self.enable_partition_pruning
#         elif i == 11:
#             return self.enable_partitionwise_join
#         elif i == 12:
#             return self.enable_partitionwise_aggregate
#         elif i == 13:
#             return self.enable_tidscan
#         else:
#             raise ValueError('Hint index out of bounds')

#     def get_name(self, i):
#         if i == 0:
#             return 'enable_hashjoin'
#         elif i == 1:
#             return 'enable_mergejoin'
#         elif i == 2:
#             return 'enable_nestloop'
#         elif i == 3:
#             return 'enable_indexscan'
#         elif i == 4:
#             return 'enable_seqscan'
#         elif i == 5:
#             return 'enable_indexonlyscan'
#         elif i == 5:
#             return 'enable_memoize'
#         elif i == 6:
#             return 'enable_gathermerge'
#         elif i == 7:
#             return 'enable_hashagg'
#         elif i == 8:
#             return 'enable_incremental_sort'
#         elif i == 9:
#             return 'enable_material'
#         elif i == 10:
#             return 'enable_partition_pruning'
#         elif i == 11:
#             return 'enable_partitionwise_join'
#         elif i == 12:
#             return 'enable_partitionwise_aggregate'
#         elif i == 13:
#             return 'enable_tidscan'
#         else:
#             raise ValueError('Hint index out of bounds')

#     def set_hints_boolean(self, boolean_list):
#         if not isinstance(boolean_list, list):
#             raise ValueError('No list provided for setting boolean hints')
#         if len(boolean_list) != len(HintSet.operators):
#             raise ValueError(
#                 'Boolean list length {} not supported for supported hints'.format(len(boolean_list)))
#         for index in range(len(boolean_list)):
#             index_element = boolean_list[index]
#             if boolean_list[index] not in [True, False]:
#                 raise ValueError(
#                     'Boolean hint list contains non boolean values')
#             self.set_hint_i(index, index_element)
#         return

#     def set_from_int_list(self, int_list):
#         for i in range(len(int_list)):
#             integer = int_list[i]
#             if integer not in [0, 1]:
#                 raise ValueError(
#                     'Setting Hint Set with values other than 0 or 1')
#             else:
#                 self.set_hint_i(i, bool(integer))
#         return

#     def get_binary_name(self):
#         binary = [int(self.get(i)) for i in range(self.hint_set_size)]
#         return binary

#     def get_int_name(self):
#         bin_list = self.get_binary_name()
#         return int("".join(str(i) for i in bin_list), 2)
