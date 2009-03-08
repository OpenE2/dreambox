package org.opendreambox.dms;

import javax.swing.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.IOException;

/**
 * Manages incoming TCP connections for dreambox messages.
 */
public class ConnectionManager extends Thread {
	/** Logger. */
	private static Logger logger = Logger.getLogger(ConnectionManager.class.getName());
	
	private ServerSocket serverSocket;
	private HashMap<String, Receiver> receivers = new HashMap<String, Receiver>();

	public ConnectionManager(ServerSocket serverSocket) {
		this.serverSocket = serverSocket;
		logger.severe("starting connection manager");
		start();
	}

	@Override
	public void run() {
		while (true) {
			try {
				logger.severe("adding receiver");
				Receiver receiver = new Receiver(serverSocket.accept());
				receivers.put(receiver.getPassword(), receiver);
				logger.severe("added receiver " + receiver.getPassword());
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	Receiver getReceiver(String password) {
		for (String receiver : receivers.keySet()) {
			logger.info("i know receiver " + receiver);
		}

		Receiver receiver = receivers.get(password);

		if (receiver == null) {
			return null;
		}

		// check if receiver is still connected
		if (receiver.isConnected()) {
			return receiver;
		} else {
			receivers.remove(password);
			return null;
		}
	}

	public void close() {
		try {
			serverSocket.close();
			for (Receiver receiver : receivers.values()) {
				receiver.close();
			}
		} catch (IOException e) {}
	}
}
