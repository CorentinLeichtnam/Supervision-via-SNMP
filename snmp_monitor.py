from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

class SNMPMonitor:
    def __init__(self, ip, community="public", port=161):
        """
        Initialise une session SNMP.
        :param ip: Adresse IP de l'équipement.
        :param community: Communauté SNMP (par défaut : public).
        :param port: Port SNMP (par défaut : 161).
        """
        self.ip = ip
        self.community = community
        self.port = port

    def get_snmp_data(self, oid):
        """
        Récupère la valeur associée à un OID via SNMP.
        :param oid: L'OID SNMP à interroger.
        :return: La valeur associée à l'OID ou None en cas d'erreur.
        """
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.ip, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )

            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

            if errorIndication:
                print(f"SNMP Error: {errorIndication}")
                return None
            elif errorStatus:
                print(f"SNMP Error: {errorStatus.prettyPrint()}")
                return None
            else:
                for varBind in varBinds:
                    return str(varBind[1])  # Retourne la valeur associée à l'OID
        except Exception as e:
            print(f"SNMP Exception: {e}")
            return None
