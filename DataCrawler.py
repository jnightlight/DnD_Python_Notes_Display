class DataCrawler:
    master_list = []
    iterator_list = []
    current_ind = 0
    master_list_size = 0

    def loadMasterList(self, new_master_list):
        self.master_list_size = self.countMasterListRecursive(new_master_list)
        return

    def countMasterListRecursive(self, new_master_list):
        #find out how many keys the top level takes up
        cur_level_keys = len(new_master_list)
        sub_keys = 0
        for sub_level_dict in new_master_list:
            for key in sub_level_dict.keys():
                sub_keys = self.countMasterListRecursive(sub_level_dict[key])
        return cur_level_keys + sub_keys