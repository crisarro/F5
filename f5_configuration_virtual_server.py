ip_protocol = ["3pc", "crdup", "ggp", "ip", "irtp", "mux", "rsvp", "sps", "uti", "a/n", "crtp", "gmtp", "ipcomp",
               "isis", "narp", "rsvp-e2e-ignore", "srp", "vines", "ah", "dccp", "", "gre", "ipcv", "iso-ip", "netblt",
               "rvd", "sscopmce", "visa", "any", "dcn", "hip", "ipencap", "iso-tp4", "nsfnet-igp", "sat-expak", "st",
               "vmtp", "argus", "ddp", "hmp", "ipip", "kryptolan", "nvp", "sat-mon", "stp", "vrrp", "aris", "ddx",
               "hopopt", "iplt", "l2tp", "ospf", "scc-sp", "sun-nd", "wb-expak", "ax.25", "dgp", "i-nlsp", "ippc",
               "larp", "pgm", "scps", "swipe", "wb-mon", "bbn-rcc", "dsr", "iatp", "ipv6", "leaf-1", "pim", "sctp",
               "tcf", "wesp", "bna", "egp", "icmp", "ipv6-auth", "leaf-2", "pipe", "sdrp", "tcp", "wsn", "br-sat-mon",
               "eigrp", "idpr", "ipv6-crypt", "manet", "pnni", "secure-vmtp", "tlsp", "xnet", "cbt", "emcon",
               "idpr-cmtp", "ipv6-frag", "merit-inp", "prm", "shim6", "tp++", "xns-idp", "cftp", "encap", "idrp",
               "ipv6-icmp", "mfe-nsp", "ptp", "skip", "trunk-1", "xtp", "chaos", "esp", "ifmp", "ipv6-nonxt", "micp",
               "pup", "sm", "trunk-2", "compaq-peer", "etherip", "igmp", "ipv6-opts", "mobile", "pvp", "smp", "ttp",
               "cphb", "fc", "igp", "ipv6-route", "mpls-in-ip", "qnx", "snp", "udp", "cpnx", "fire", "il", "ipx-in-ip",
               "mtp", "rdp", "sprite-rpc", "udplite"]

load_balance_list = ["dynamic-ratio-member", "least-connections-node", "predictive-node", "ratio-session",
                     "dynamic-ratio-node", "least-sessions", "ratio-least-connections-member", "round-robin",
                     "fastest-app-response", "observed-member", "ratio-least-connections-node",
                     "weighted-least-connections-member", "fastest-node", "observed-node", "ratio-member",
                     "weighted-least-connections-node", "least-connections-member", "predictive-member", "ratio-node"]

other_options_list = ["min-up-members", "min-active-members", "min-up-members-action", "min-up-members-checking"]

member_option_specific_list = ["state", "dynamic-ratio", "priority-group", "ratio"]


class F5_virtual_server:

    def __init__(self, URL_name, VIP, port, pool_name, virtual_server_name, destination, description, connection_limit):

        self.URL_name = input("what is the name of the URL? \n")
        self.VIP = input("What is the VIP? \n")
        self.port = input("what is the service port? \n")
        self.pool_name = f"/Common/pl_{self.URL_name}_{self.port}"
        self.virtual_server_name = f"vs_{self.URL_name}_{self.port}"
        self.destination = f'{self.VIP}:{self.port}'
        self.description = input("Enter the description \n")
        self.connection_limit = input("What is the connection limit? \n")

    def partition_func(self):

        partition_while = True
        while partition_while:
            print("is the partition Common(Y/N)")
            partition_question = input()

            if partition_question == "Y":
                self.partition = "Common"
                break
                partition_while = False

            if partition_question == "N":
                print("What is the name of the partition?")
                self.partition = input()
                break
                partition_while = False

            if partition_question != "Y" or partition_question != "N":
                print("Available options are Y/N")

    def encryption_func(self):

        reencryption = True
        while reencryption:

            print("Do you need SSL offloading or re-encryption?(Y/N)")
            encryption_need = input()

            if encryption_need == "Y":
                clientssl = f" /Common/pr-sscli_{self.URL_name} {{ context clientside }}"
                break
                reencryption = False

            if encryption_need == "N":
                serverside = "N"
                print("No SSL need")
                break
                reencryption = False

            if encryption_need != "Y" or encryption_need != "N":
                print("Available options are Y/N")

        SSL = True
        while SSL:

            if encryption_need == "N":
                serverssl_ssl = ""
                break
                SSL = False

            print("Do you need serverside SSL (Y/N)")
            serverside = input()
            if serverside == "Y":
                print("is the profile name serverssl_default? (Y/N)")
                serverssl = input()

                if serverssl == "Y":
                    print("Let's use that one then")
                    serverssl_ssl = "/Common/serverssl_default"
                    break
                    SSL = False

                if serverssl == "N":
                    print("What is the name of the serverside profile(Include partition, example: /Common/)")
                    serverssl_ssl = input()
                    break
                    SSL = False

                if serverssl != "Y" or serverssl != "N":
                    print("Available options are Y/N")

            if serverside == "N":
                print("No serverside is need")
                break
                SSL = False

            if serverside != "Y" or serverside != "N":
                print("Available options are Y/N")

        if serverside == "Y":
            serverSSL = f"{serverssl_ssl} {{ context serverside }}"

        if serverside == "N":
            serverSSL = ""

        if encryption_need == "Y":
            self.SSL_PROFILE = f"profiles add {{ {clientssl} {serverSSL} }}"
        if encryption_need == "N":
            serverSSL = None
            self.SSL_PROFILE = ""

    def profile_func(self):
        profile = True
        profile_list = []
        while profile:
            print("Do you need any other profile(Y/N)?(example http)")
            profile_q = input()

            if profile_q == "Y":
                print("what is the name of the profile")
                profile_need = input()
                profile_list.append(f'profiles add {{ {profile_need} }}')

            if profile_q == "N":
                print("No more profiles neeed")
                break
                profile = False

            if profile_q != "Y" or profile_q != "N":
                print("Available options are Y/N")

        if profile_list == []:
            self.join_list_profile = ""

        if profile_list != []:
            self.join_list_profile = " ".join(profile_list)

    def persistance_func(self):
        persistance = True
        while persistance:
            print("Do you need persistance profile(Y/N)")
            persistance_option = input()

            if persistance_option == "Y":
                print("what is the name of the profile")
                persistance_config = input()
                break
                persistance = False

            if persistance_option == "N":
                print("No persistance profiles neeed")
                break
                persistance = False

            if persistance_option != "Y" or persistance_option != "N":
                print("Available options are Y/N")

        if persistance_option == "Y":
            self.Apply_persistance = f"persist replace-all-with {{ {persistance_config} }}"

        if persistance_option == "N":
            self.Apply_persistance = ""

    def protocol_func(self):
        protocol = True
        while protocol:
            print("what is the ip-protocol")
            self.ipprotocol = input()

            if self.ipprotocol in ip_protocol:
                self.ipprotocol
                break

            else:
                print("Here are the available options")
                for n in ip_protocol:
                    print(n)

    def vs_config(self):
        print("\n")
        print("Here is the virtual server configuration command ")
        print("\n")
        return f"cd /{self.partition} \ncreate ltm virtual {self.virtual_server_name} description {self.description} destination {self.destination} ip-protocol {self.ipprotocol} {self.join_list_profile} pool {self.pool_name} connection-limit {self.connection_limit} {self.SSL_PROFILE} {self.Apply_persistance} source-address-translation {{ type automap }} translate-address enabled translate-port enabled"

    def first_members_func(self):
        print("\n")
        print("Pool configuration")
        print("\n")

        first_member_list = []
        first_member_dict = {}

        print("What is the member IP address? ")
        self.key_address = input()

        print("what is the member port")
        self.value_port = input()

        first_member_dict[self.key_address] = self.value_port

        first_member_option_list = []
        first_member_options = True
        while first_member_options:

            member_other_options = input("Do you need additional member options for the pool member?(Y/N) ")

            if member_other_options == "Y":
                print("Available options are")
                for item in member_option_specific_list:
                    print(item)
                option = input("Enter the option ")

                if option == "state":
                    state_options = input("Available options user-down/user-up")
                    self.state_option = f"state {state_options}"
                    first_member_option_list.append(self.state_option)

                if option == "dynamic-ratio":
                    dynamic_ratio_option = int(input("Enter the value "))
                    self.dynamic_ratio = f"dynamic-ratio {dynamic_ratio_option}"
                    first_member_option_list.append(self.dynamic_ratio)

                if option == "priority-group":
                    priority_group_option = int(input("Enter the value "))
                    self.priority_group = f"priority-group {priority_group_option}"
                    first_member_option_list.append(self.priority_group)

                if option == "ratio":
                    ratio_option = int(input("Enter the value "))
                    self.ratio = f"ratio {ratio_option}"
                    first_member_option_list.append(self.ratio)

                if option not in member_option_specific_list:
                    print("Please try again")

            self.join_member_option_list = " ".join(first_member_option_list)

            if member_other_options == "N":
                print("No more member options need")
                break
                first_member_options = False

        first_member_list.append(
            f"members add {{ {self.key_address}:{self.value_port}  {{ address {self.key_address} {self.join_member_option_list} session user-enabled }} }}")

        self.join_first_member_list = " ".join(first_member_list)

    def members_func(self):
        try:
            print("is the port the same for all the members? (Y/N/single)")
            same_port = input()

            if same_port == "Y":
                members = False
                same_port_path = True

            if same_port == "N":
                members = True
                same_port_path = False

            if same_port == "single":
                members = False
                same_port_path = False
                print("No more members need")

            else:
                print("Available options are Y/N/single")

            members_list = []
            members_dict = {}
            count_1 = 0
            while members:

                if count_1 == 0:
                    new_member = "Y"

                if count_1 > 0:
                    print("Do you need more members ? Y/N")
                    new_member = input()

                count_1 += 1
                if new_member == "Y":
                    print("What is the member IP address? ")
                    key_address = input()

                    print("what is the member port")
                    value_port = input()
                    members_dict[key_address] = value_port

                    pl_member_option_list = []
                    options = True
                    while options:

                        member_other_options = input("Do you need additional member options for the pool member?(Y/N) ")

                        if member_other_options == "Y":
                            print("Available options are")
                            for item in member_option_specific_list:
                                print(item)

                            option = input("Enter the option ")

                            if option == "state":
                                state_options = input("Available options user-down/user-up")
                                self.state_option = f"state {state_options}"
                                pl_member_option_list.append(self.state_option)

                            if option == "dynamic-ratio":
                                dynamic_ratio_option = int(input("Enter the value "))
                                self.dynamic_ratio = f"dynamic-ratio {dynamic_ratio_option}"
                                pl_member_option_list.append(self.dynamic_ratio)

                            if option == "priority-group":
                                priority_group_option = int(input("Enter the value "))
                                self.priority_group = f"priority-group {priority_group_option}"
                                pl_member_option_list.append(self.priority_group)

                            if option == "ratio":
                                ratio_option = int(input("Enter the value "))
                                self.ratio = f"ratio {ratio_option}"
                                pl_member_option_list.append(self.ratio)

                            if option not in member_option_specific_list:
                                print("Please try again")

                        self.join_member_option_list = " ".join(pl_member_option_list)

                        if member_other_options == "N":
                            print("No more member options need")
                            break
                            options = False

                members_list.append(
                    f"members add {{ {key_address}:{value_port}  {{ address {key_address} {self.join_member_option_list} session user-enabled }} }}")

                if new_member == "N":
                    print("No more members need")
                    break
                    members = False

                else:
                    print("Available options are Y/N")

            count = 0
            while same_port_path:

                if count == 0:
                    new_member = "Y"

                if count > 0:
                    print("Do you need more members ? Y/N")
                    new_member = input()

                count += 1
                if new_member == "Y":
                    print("What is the member IP address? ")
                    key_address = input()
                    members_dict[key_address] = self.value_port
                    pl_member_option_list = []
                    options = True
                    while options:

                        member_other_options = input("Do you need additional member options for the pool member?(Y/N) ")

                        if member_other_options == "Y":
                            print("Available options are")
                            for item in member_option_specific_list:
                                print(item)

                            option = input("Enter the option ")

                            if option == "state":
                                state_options = input("Available options user-down/user-up")
                                self.state_option = f"state {state_options}"
                                pl_member_option_list.append(self.state_option)

                            if option == "dynamic-ratio":
                                dynamic_ratio_option = int(input("Enter the value "))
                                self.dynamic_ratio = f"dynamic-ratio {dynamic_ratio_option}"
                                pl_member_option_list.append(self.dynamic_ratio)

                            if option == "priority-group":
                                priority_group_option = int(input("Enter the value "))
                                self.priority_group = f"priority-group {priority_group_option}"
                                pl_member_option_list.append(self.priority_group)

                            if option == "ratio":
                                ratio_option = int(input("Enter the value "))
                                self.ratio = f"ratio {ratio_option}"
                                pl_member_option_list.append(self.ratio)

                            if option not in member_option_specific_list:
                                print("Please try again")

                        self.join_member_option_list = " ".join(pl_member_option_list)

                        if member_other_options == "N":
                            print("No more member options need")
                            break
                            options = False

                members_list.append(
                    f"members add {{ {key_address}:{self.value_port}  {{ address {key_address} {self.join_member_option_list} session user-enabled }} }}")

                if new_member == "N":
                    print("No more members need")
                    break
                    members = False

                else:
                    print("Available options are Y/N")

            if members_list == []:
                self.join_list_members = ""

            members_list.pop()
            self.join_list_members = " ".join(members_list)


        except IndexError:
            pass

    def load_balancing_mode_func(self):
        load = True
        while load:
            print("What is the load balance method? ")
            self.load_balance_method = input()

            if self.load_balance_method in load_balance_list:
                self.load_balance_method
                break

            else:
                print("Here are the available options")
                for n in load_balance_list:
                    print(n)

    def pool_other_options_func(self):
        pl_globlal_option_list = []
        optional = True

        while optional:
            self.additional_option_list = []

            other_options = input("Do you need additional options for the pool?(Y/N) ")

            if other_options == "Y":
                print("Available options are")
                for item in other_options_list:
                    print(item)

                option = input("Enter the option ")

                if option == "min-up-members":
                    min_up_members_option = int(input("Enter the value "))
                    self.min_up_members_option = f"min-up-members {min_up_members_option}"
                    pl_globlal_option_list.append(self.min_up_members_option)

                if option == "min-active-members":
                    min_active_members_option = int(input("Enter the value "))
                    self.min_active_members = f"min-active-members {min_active_members_option}"
                    pl_globlal_option_list.append(self.min_active_members)

                if option == "min-up-members-checking":
                    min_up_members_checking_option = input("Available options disabled/enabled ")
                    self.min_up_members_checking_option = f"min-up-members-checking {min_up_members_checking_option}"
                    pl_globlal_option_list.append(self.min_up_members_checking_option)

                if option == "min-up-members-action":
                    min_up_members_action_options = input("Available options failover/reboot/restart-all ")
                    self.min_up_members_action = f"min-up-members-action {min_up_members_action_options}"
                    pl_globlal_option_list.append(self.min_up_members_action)

                if option not in other_options_list:
                    print("please try again")

            if other_options == "N":
                print("No more options need")
                break
                optional = False

        self.join_pl_globlal_option_list = " ".join(pl_globlal_option_list)

    def monitor_func(self):
        self.monitor = input("Enter the monitor ")

    def pl_config(self):
        print("\n")
        print("Here is the pool configuration command ")
        print("\n")
        return f"cd /{self.partition} \n create ltm pool pl_{self.URL_name}_{self.port} description {self.description}  load-balancing-mode {self.load_balance_method} {self.join_first_member_list} {self.join_list_members} {self.join_pl_globlal_option_list} monitor {self.monitor} "

    def vs_ssl_profile(self):
        print("\n")
        print("Here is the SSL client profile configuration command ")
        print("\n")
        return f"create ltm profile client-ssl pr-sscli_{self.URL_name} {{ app-service none cert {self.URL_name}_2021.crt cert-key-chain add {{ {self.URL_name}_2021_intermediate-ca {{ cert {self.URL_name}_2021.crt chain intermediate-ca.crt key {self.URL_name}_2021.key }} }} chain intermediate-ca.crt defaults-from clientssl key {self.URL_name}_2021.key passphrase none }} "


K = F5_virtual_server("URL_name", "VIP", "port", "pool_name", "virtual_server_name", "destination", "description",
                      "connection_limit")

K.partition_func()
K.encryption_func()
K.profile_func()
K.persistance_func()
K.protocol_func()

K.first_members_func()
K.members_func()
K.pool_other_options_func()
K.load_balancing_mode_func()
K.monitor_func()

print(K.vs_ssl_profile())
print(K.pl_config())
print(K.vs_config())
