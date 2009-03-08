package org.opendreambox.dms;

import java.net.Socket;
import java.io.*;
import java.util.logging.Logger;
import java.util.ArrayList;

/**
 * Receiver of dreambox messages.
 */
public class Receiver {
	/** Logger. */
	private static Logger logger = Logger.getLogger(Receiver.class.getName());

	private String password;
	private Socket socket;
	private BufferedWriter w;
	private BufferedReader r;

	public Receiver(Socket socket) throws IOException {
		this.socket = socket;
		logger.info("Receiver created, weiting for password...");

		// create streams
		r = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		w = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
		// read passwort (used as client id) from receiver
		password = r.readLine().trim();

		logger.info("... got password");
	}

	public String getPassword() {
		return password;
	}

	public void sendMessage(String message) throws IOException, ReceiverException {
		flushReader(r);

		w.write("message;");
		w.write(encode(message) + "\r\n");
		w.flush();

		String returnString = r.readLine().trim();
		if (!returnString.equals("OK")) {
			throw new ReceiverException(returnString);
		}
	}

	public String sendQuestion(String message, ArrayList<String> answers) throws IOException, ReceiverException {
		flushReader(r);

		w.write("question;");
		w.write(encode(message));
		for (String option : answers) {
			w.write(";" + encode(option));
		}
		w.write("\r\n");
		w.flush();

		String returnString = r.readLine().trim();
		if (!returnString.equals("OK")) {
			throw new ReceiverException(returnString);
		}

		return r.readLine().trim();
	}

	private void flushReader(BufferedReader r) throws IOException {
		while (r.ready()) r.read();
	}

	private String encode(String text) {
		return text.trim().replace(';',',').replaceAll("\n", "\\\\n");
	}

	public boolean isConnected() {
		return socket.isConnected();
	}

	public void close() {
		try {
			socket.close();
		} catch (IOException e) {}
	}
}
